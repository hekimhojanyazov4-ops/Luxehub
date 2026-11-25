from django.contrib import admin
from .models import (User, Room, Reservation, Payment, Review, Favourite)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'phone', 'role', 'first_name', 'last_name', 'created_at', 'updated_at']