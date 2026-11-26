
from django.contrib import admin

from .models import (
    Favourite,
    NewsLetterSubscriber,
    Payment,
    Reservation,
    Review,
    Room,
    RoomImage,
    User
)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'is_staff', 'first_name', 'last_name', 'email', 'phone', 'role', 'is_email_verified']
    list_per_page = 20

# ---------------------------------------------------------------------
# Rooms
# ---------------------------------------------------------------------

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_type', 'number', 'price_per_night', 'capacity', 'discount_price_per_night', 'is_active']
    list_per_page = 20
    


@admin.register(RoomImage)
class RoomImageAdmin(admin.ModelAdmin):
    list_display = ['room', 'image', 'is_primary', 'created_at', 'updated_at']
    list_per_page = 20


# ---------------------------------------------------------------------
# Reservations
# ---------------------------------------------------------------------

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['room', 'user', 'nights', 'check_in', 'check_out', 'guests_count', 'total_price', 'status']
    list_per_page = 20


# ---------------------------------------------------------------------
# Payments
# ---------------------------------------------------------------------

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['reservation', 'amount', 'method', 'status', 'transaction_id', 'paid_at']
    list_per_page = 20


# ---------------------------------------------------------------------
# Favourites
# ---------------------------------------------------------------------

@admin.register(Favourite)
class FavouriteAdmin(admin.ModelAdmin):
    list_display = ['room', 'user']
    list_per_page = 20


# ---------------------------------------------------------------------
# Reviews
# ---------------------------------------------------------------------

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['comment', 'user', 'room', 'stars']
    list_per_page = 20


# ---------------------------------------------------------------------
# Newsletter
# ---------------------------------------------------------------------

@admin.register(NewsLetterSubscriber)
class NewsLetterSubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'is_active']
    list_per_page = 20
