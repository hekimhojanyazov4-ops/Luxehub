import uuid

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as DjangoUserManager
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
from django.db.models import Q
from django.db.models.constraints import UniqueConstraint
from django.utils import timezone

PHONE_REGEX = r'^\+993(61|62|63|64|65|71|72)\d{6}$'
PHONE_MESSAGE = (
    "Telefon belgisi +993 bilen başlap, 61,62,63,64,65,71,72 operator "
    "kodlarynyň birini we 6 sanly abonent nomerini öz içine almaly."
)
phone_validator = RegexValidator(regex=PHONE_REGEX, message=PHONE_MESSAGE)


class Base(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserManager(DjangoUserManager):
    """
    BUG FIX: create_user / create_superuser used to call
    `super()._create_user(...)`, which skips this class's own
    `_create_user` override entirely (it calls Django's base
    implementation directly). They now call `self._create_user(...)`
    so the email/phone validation below always runs.
    """

    def _create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email hökmany girizilmeli.")
        phone = extra_fields.get('phone')
        if not phone:
            raise ValueError("Telefon belgisi girizilmeli.")

        email = self.normalize_email(email).strip().lower()
        extra_fields["phone"] = phone.strip()
        return super()._create_user(username, email, password, **extra_fields)

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('role', self.model.Role.CUSTOMER)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', self.model.Role.ADMIN)
        extra_fields['is_email_verified'] = True

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser üçin is_staff=True bolmaly.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser üçin is_superuser=True bolmaly.')

        return self._create_user(username, email, password, **extra_fields)


class User(Base, AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", 'Admin'
        MANAGER = "MANAGER", "Manager"
        CUSTOMER = "CUSTOMER", "Customer"

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.CUSTOMER)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    phone = models.CharField(max_length=13, validators=[phone_validator], unique=True)
    is_email_verified = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['email', 'phone', 'first_name', 'last_name']

    objects = UserManager()

    @property
    def is_customer(self):
        return self.role == self.Role.CUSTOMER

    @property
    def is_staff_role(self):
        return self.role in (self.Role.ADMIN, self.Role.MANAGER)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class Room(Base):
    class RoomType(models.TextChoices):
        SINGLE = "SINGLE", "Single"
        DOUBLE = "DOUBLE", "Double"
        DELUXE = "DELUXE", "Deluxe"
        SUITE = "SUITE", "Suite"

    room_type = models.CharField(max_length=20, choices=RoomType.choices, default=RoomType.SINGLE)
    description = models.TextField()
    number = models.PositiveIntegerField(db_index=True, unique=True)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    # BUG FIX: had no default/null option, making every room require a
    # discount price even when it has none. Now optional.
    discount_price_per_night = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    capacity = models.PositiveIntegerField(
        default=1, validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['number']

    def __str__(self):
        return f"{self.number}"

    def clean(self):
        super().clean()
        if (
            self.discount_price_per_night is not None
            and self.discount_price_per_night >= self.price_per_night
        ):
            raise ValidationError(
                {"discount_price_per_night": "Arzanladylan baha adaty bahadan pes bolmaly."}
            )

    def is_available_for(self, check_in, check_out, exclude_reservation_id=None):
        if not self.is_active:
            return False

        overlapping = Reservation.objects.filter(
            room=self,
            status__in=[
                Reservation.Status.PENDING,
                Reservation.Status.CONFIRMED,
            ],
            check_in__lt=check_out,
            check_out__gt=check_in,
        )
        if exclude_reservation_id:
            overlapping = overlapping.exclude(pk=exclude_reservation_id)

        return not overlapping.exists()


class RoomImage(Base):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='images')
    # BUG FIX: unnecessary/misleading f-string with no placeholder.
    image = models.ImageField(upload_to="room_images/")
    is_primary = models.BooleanField(default=False)

    class Meta:
        ordering = ['-is_primary', '-created_at']

    def __str__(self):
        return f"{self.room.number} image"

    def save(self, *args, **kwargs):
        # Only one primary image per room.
        if self.is_primary:
            RoomImage.objects.filter(room=self.room, is_primary=True).exclude(
                pk=self.pk
            ).update(is_primary=False)
        super().save(*args, **kwargs)


class Reservation(Base):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        CONFIRMED = "CONFIRMED", "Confirmed"
        CANCELLED = "CANCELLED", "Cancelled"
        COMPLETED = "COMPLETED", "Completed"

    # BUG FIX: limit_choices_to={User.Role.CUSTOMER} is a set literal, not a
    # valid filter — it never actually restricted anything. Correct form is
    # a dict: {"role": User.Role.CUSTOMER}.
    user = models.ForeignKey(
        User,
        limit_choices_to={"role": User.Role.CUSTOMER},
        related_name='reservations',
        on_delete=models.PROTECT,
    )
    # BUG FIX: related_name was 'rooms', which reads backwards
    # (room.reservations.all() is the natural name).
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='reservations')
    check_in = models.DateField()
    check_out = models.DateField()
    guests_count = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    total_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False, default=0)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)

    class Meta:
        ordering = ['-created_at']
        constraints = [
            UniqueConstraint(
                fields=['user'],
                condition=Q(status='PENDING'),
                name='one_pending_reservation_per_customer',
            ),
        ]

    @property
    def nights(self):
        if self.check_in and self.check_out and self.check_out > self.check_in:
            return (self.check_out - self.check_in).days
        return 0

    def clean(self):
        # BUG FIX: was `super.clean()` (missing the call parentheses on
        # `super()`), which raises an AttributeError instead of calling
        # Model.clean().
        super().clean()

        if self.check_in and self.check_in < timezone.localdate():
            raise ValidationError({"check_in": "Geçen senä otag bronlap bolmaz."})

        if self.check_in and self.check_out and self.check_out <= self.check_in:
            raise ValidationError(
                {"check_out": "Çykyş senesi hökman giriş senesinden soň bolmaly."}
            )

        # BUG FIX: condition was reversed (`<` instead of `>`) — it was
        # rejecting reservations with FEWER guests than capacity, the
        # opposite of the intended rule.
        if self.room_id and self.guests_count > self.room.capacity:
            raise ValidationError(
                {"guests_count": f"Bu otag iň köp {self.room.capacity} myhman kabul edip bilýär."}
            )

        if (
            self.room_id
            and self.check_in
            and self.check_out
            # BUG FIX: `self.status.PENFING` was both a typo (PENFING) and
            # wrong target (`self.status` is the current string value, not
            # the Status class). Correct reference is `self.Status.PENDING`.
            and self.status in [self.Status.PENDING, self.Status.CONFIRMED]
        ):
            if not self.room.is_available_for(
                self.check_in, self.check_out, exclude_reservation_id=self.pk
            ):
                raise ValidationError("Bu otag saýlanan senelerde eýýäm bronlanan.")

    def save(self, *args, **kwargs):
        if self.check_in and self.check_out and self.check_out > self.check_in and self.room_id:
            nights = (self.check_out - self.check_in).days
            self.total_price = nights * self.room.price_per_night
        self.full_clean()
        # BUG FIX: `super().save(*args, *kwargs)` unpacked kwargs with a
        # single `*`, which fails for a dict. Needs `**kwargs`.
        super().save(*args, **kwargs)

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

    # BUG FIX: related_name was 'payments' on a OneToOneField, which is
    # misleading (there can only ever be one). Singular 'payment' matches
    # how it's actually used: reservation.payment
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=20, choices=Method.choices, default=Method.CARD)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    transaction_id = models.CharField(max_length=100, blank=True, null=True, unique=True)
    paid_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Payment {self.amount} for {self.reservation} [{self.get_status_display()}]"


class Favourite(Base):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='favourites')
    user = models.ForeignKey(User, related_name='favourites', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(fields=['user', 'room'], name='unique_user_room_favourite')
        ]

    def __str__(self):
        return f"{self.room.number} by {self.user.username}"


class Review(Base):
    comment = models.TextField()
    # BUG FIX: same limit_choices_to set-literal bug as Reservation.user.
    user = models.ForeignKey(
        User,
        related_name='reviews',
        on_delete=models.CASCADE,
        limit_choices_to={"role": User.Role.CUSTOMER},
    )
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