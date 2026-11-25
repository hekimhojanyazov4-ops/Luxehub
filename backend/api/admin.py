
from django.contrib import admin

from .models import (
    Favourite,
    NewsLetterSubscriber,
    Payment,
    Reservation,
    Review,
    Room,
    RoomImage,
)


# ---------------------------------------------------------------------
# Rooms
# ---------------------------------------------------------------------

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_per_page = 20


@admin.register(RoomImage)
class RoomImageAdmin(admin.ModelAdmin):
    list_per_page = 20


# ---------------------------------------------------------------------
# Reservations
# ---------------------------------------------------------------------

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_per_page = 20


# ---------------------------------------------------------------------
# Payments
# ---------------------------------------------------------------------

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_per_page = 20


# ---------------------------------------------------------------------
# Favourites
# ---------------------------------------------------------------------

@admin.register(Favourite)
class FavouriteAdmin(admin.ModelAdmin):
    list_per_page = 20


# ---------------------------------------------------------------------
# Reviews
# ---------------------------------------------------------------------

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_per_page = 20


# ---------------------------------------------------------------------
# Newsletter
# ---------------------------------------------------------------------

@admin.register(NewsLetterSubscriber)
class NewsLetterSubscriberAdmin(admin.ModelAdmin):
    list_per_page = 20
