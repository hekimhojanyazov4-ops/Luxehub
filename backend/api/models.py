import uuid
from django.db import models
from django.contrib.auth.models import UserManager as DjangoUserManager
from django.contrib.auth.models import AbstractUser
import re
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.db.models.constraints import UniqueConstraint
from django.db.models import Q


PHONE_REGEX = r'^\+993(61|62|63|64|65|71|72)\d{6}$'
PHONE_MESSAGE = (
    "Telefon belgisi +993 bilen başlap, 61,62,63,64,65,71,72 operator "
    "kodlarynyň birini we 6 sanly abonent nomerini öz içine almaly."
)
phone_validator = RegexValidator(regex=PHONE_REGEX, message=PHONE_MESSAGE)



class Base(models.Model):
    id = models.UUIDField(unique=True, editable=False, primary_key=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True



class UserManager(DjangoUserManager):

    def _create_user(self, username, email, password = None, **extra_fields):
        if not email:
            raise ValueError("Email hokmany girizilmeli.")
        phone = extra_fields.get('phone')
        if not phone:
            raise ValueError("Telefon belgisi girizilmeli")
        
        email = self.normalize_email(email).strip().lower()
        extra_fields["phone"] = phone.strip()
        return super()._create_user(username, email, password, **extra_fields)


    def create_user(self, username, email = None, password = None, **extra_fields):
        extra_fields.setdefault('role', self.model.Role.CUSTOMER)
        return super()._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email = None, password = None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', self.model.Role.ADMIN)
        extra_fields['is_email_verified'] = True

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser üçin is_staff=True bolmaly.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser üçin is_superuser=True bolmaly.')
        
        return super()._create_user(username, email, password, **extra_fields)


class User(Base, AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", 'Admin'
        MANAGER = "MANAGER", "Manager"
        CUSTOMER = "CUSTOMER", "Customer"

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.CUSTOMER)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    phone = models.CharField(max_length=13, validators=[phone_validator], unique = True)
    is_email_verified = models.BooleanField(default=False)
    REQUIRED_FIELDS = ['email', 'phone', 'first_name', 'last_name']
    

    objects = UserManager()

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


    

class Room(Base):
    class RoomType(models.TextChoices):
        SINGLE = "SINGLE", "Single"
        DOUBLE = "DOUBLE", "Double"
        DELUXE = "DELUXE", "Deluxe"
        SUITE = "SUITE", "Suite"
    room_type = models.CharField(max_length = 20, choices = RoomType.choices, default = RoomType.SINGLE)
    description = models.TextField()
    number = models.PositiveIntegerField(db_index=True, unique = True)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price_per_night = models.DecimalField(max_digits=10,decimal_places=2)
    capacity = models.PositiveIntegerField(default=1, validators = [MinValueValidator(1), MaxValueValidator(10)])
    is_active = models.BooleanField(default = True)

    class Meta:
        ordering = ['number']
    

    def __str__(self):
        return f"{self.number}"

    def is_available_for(self, check_in, check_out, exclude_reservation_id = None):
        if not self.is_active:
            return False

        overlapping = Reservation.objects.filter(
            room = self,
            status__in = [
                Reservation.Status.PENDING,
                Reservation.Status.CONFIRMED,
            ],
            check_in__lt = check_out,
            check_out__gt = check_in,
        )
        if exclude_reservation_id:
            overlapping = overlapping.exclude(pk = exclude_reservation_id)

        return not overlapping.exists()

class RoomImage(Base):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=f"room_images/")
    is_primary = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.room.number} image"




class Reservation(Base):
    class Status(models.TextChoices):
        PENDING = "PENDING" , "Pending"
        CONFIRMED = "CONFIRMED", "Confirmed"
        CANCELLED = "CANCELLED", "Cancelled"
        COMPLETED = "COMPLETED", "Completed"

    user = models.ForeignKey(User, limit_choices_to={User.Role.CUSTOMER}, related_name='reservations', on_delete=models.PROTECT)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='rooms')
    check_in = models.DateField()
    check_out = models.DateField()
    guests_count = models.PositiveIntegerField(default = 1, validators = [MinValueValidator(1)])
    total_price = models.DecimalField(max_digits=10, decimal_places=2, editable = False, default = 0)
    status = models.CharField(max_length = 20, choices = Status.choices, default = Status.PENDING)

    class Meta:
        ordering = ['-created_at']

        constraints = [
            UniqueConstraint(
                fields = ['user'],
                condition = models.Q(status = 'PENDING'),
                name = 'one_pending_reservation_per_customer',
            ),
        ]

    def clean(self):
        super.clean()
        if self.check_in and self.check_out and self.check_out <= self.check_in:
            raise ValidationError(
                {"check_out": "Check out date is must be greater than check in date."}
            )
        if self.room.id and self.guests_count < self.room.capacity:
            raise ValidationError(
                {
                    "guests_count": (f"This room can get maximum {self.room.capacity} guests.")
                }
            )
        if (
            self.room.id
            and self.check_in
            and self.check_out
            and self.status in [self.status.PENFING, self.status.CONFIRMED]
        ):
            if not self.room.is_available_for(self.check_in, self.check_out, exclude_reservation_id=self.pk):
                raise ValidationError("This room is booked for chosen dates.")

    def save(self, *args, **kwargs):
        if self.check_in and self.check_out and self.check_out > self.check_in and self.room_id:
            nights = (self.check_out - self.check_in).days
            self.total_price = nights * self.room.price_per_night
        self.full_clean()
        super().save(*args, *kwargs)

    def __str__(self):
        return f"{self.user.username} --> {self.room.number} ({self.check_in}) to {self.check_out}"






class Payment(Base):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        PAID = "PAID", "Paid"
        FAILED = "FAILED", "Failed"
        REFUNDED = "REFUNDED", "Refunded"

    class Method(models.TextChoices):
        CARD = "CARD", "Card"
        CASH = "CASH", "Cash"
        TRANSFER = "TRANSFER", "Bank Transfer"
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(
        max_length=20, choices=Method.choices, default=Method.CARD
    )
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )
    transaction_id = models.CharField(max_length=100, blank=True, null=True, unique=True)
    paid_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Payment {self.amount} for {self.reservation} [{self.get_status_display()}]"





class Favourite(Base):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='favourites')
    user = models.ForeignKey(User, related_name = 'favourites', on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields = ['user', 'room'],
                name = 'unique_user_room_favourite'
            )
        ]


    def __str__(self):
        return f"{self.room.number} by {self.user.username}"






class Review(Base):
    comment = models.TextField()
    user = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE, limit_choices_to={User.Role.CUSTOMER})
    room = models.ForeignKey(Room, related_name='reviews', on_delete=models.CASCADE)
    stars = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    class Meta:
        ordering = ['-created_at']
        unique_together = ('room', 'user')

    def __str__(self):
        return f"{self.stars} by {self.user.username}"





class NewsLetterSubscriber(Base):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email