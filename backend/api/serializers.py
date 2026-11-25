from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import (
    Favourite,
    NewsLetterSubscriber,
    Payment,
    Reservation,
    Review,
    Room,
    RoomImage,
)

User = get_user_model()


# ---------------------------------------------------------------------
# User
# ---------------------------------------------------------------------

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id", "username", "email", "first_name", "last_name",
            "phone", "role", "is_email_verified", "date_joined",
        ]
        read_only_fields = ["id", "role", "is_email_verified", "date_joined"]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "first_name", "last_name", "phone"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


# ---------------------------------------------------------------------
# Room
# ---------------------------------------------------------------------

class RoomImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomImage
        fields = ["id", "room", "image", "is_primary"]
        read_only_fields = ["id"]


class RoomSerializer(serializers.ModelSerializer):
    images = RoomImageSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = [
            "id", "room_type", "number", "description",
            "price_per_night", "discount_price_per_night", "capacity",
            "is_active", "images", "average_rating", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def get_average_rating(self, obj):
        reviews = list(obj.reviews.all())
        if not reviews:
            return None
        return round(sum(r.stars for r in reviews) / len(reviews), 1)

    def validate(self, attrs):
        price = attrs.get("price_per_night", getattr(self.instance, "price_per_night", None))
        discount = attrs.get(
            "discount_price_per_night", getattr(self.instance, "discount_price_per_night", None)
        )
        if discount is not None and price is not None and discount >= price:
            raise serializers.ValidationError(
                {"discount_price_per_night": "Arzanladylan baha adaty bahadan pes bolmaly."}
            )
        return attrs


class RoomAvailabilitySerializer(serializers.Serializer):
    check_in = serializers.DateField()
    check_out = serializers.DateField()

    def validate(self, attrs):
        if attrs["check_out"] <= attrs["check_in"]:
            raise serializers.ValidationError("check_out hökman check_in-dan soň bolmaly.")
        return attrs


# ---------------------------------------------------------------------
# Reservation
# ---------------------------------------------------------------------

class ReservationSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    room_detail = RoomSerializer(source="room", read_only=True)
    nights = serializers.ReadOnlyField()

    class Meta:
        model = Reservation
        fields = [
            "id", "user", "room", "room_detail", "check_in", "check_out",
            "guests_count", "nights", "total_price", "status", "created_at",
        ]
        read_only_fields = ["id", "user", "total_price", "status", "created_at"]

    def validate(self, attrs):
        check_in = attrs.get("check_in", getattr(self.instance, "check_in", None))
        check_out = attrs.get("check_out", getattr(self.instance, "check_out", None))
        room = attrs.get("room", getattr(self.instance, "room", None))
        guests_count = attrs.get("guests_count", getattr(self.instance, "guests_count", 1))

        if check_in and check_out and check_out <= check_in:
            raise serializers.ValidationError(
                {"check_out": "Çykyş senesi hökman giriş senesinden soň bolmaly."}
            )

        if room and guests_count and guests_count > room.capacity:
            raise serializers.ValidationError(
                {"guests_count": f"Bu otag iň köp {room.capacity} myhman kabul edip bilýär."}
            )

        if room and check_in and check_out:
            exclude_id = self.instance.pk if self.instance else None
            if not room.is_available_for(check_in, check_out, exclude_reservation_id=exclude_id):
                raise serializers.ValidationError("Bu otag saýlanan senelerde eýýäm bronlanan.")

        return attrs

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


class ReservationStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ["status"]


# ---------------------------------------------------------------------
# Payment
# ---------------------------------------------------------------------

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "id", "reservation", "amount", "method",
            "status", "transaction_id", "paid_at", "created_at",
        ]
        read_only_fields = ["id", "created_at"]


# ---------------------------------------------------------------------
# Favourite
# ---------------------------------------------------------------------

class FavouriteSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    room_detail = RoomSerializer(source="room", read_only=True)

    class Meta:
        model = Favourite
        fields = ["id", "user", "room", "room_detail", "created_at"]
        read_only_fields = ["id", "user", "created_at"]

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


# ---------------------------------------------------------------------
# Review
# ---------------------------------------------------------------------

class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ["id", "user", "room", "comment", "stars", "created_at"]
        read_only_fields = ["id", "user", "created_at"]

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


# ---------------------------------------------------------------------
# Newsletter
# ---------------------------------------------------------------------

class NewsLetterSubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsLetterSubscriber
        fields = ["id", "email", "is_active", "created_at"]
        read_only_fields = ["id", "is_active", "created_at"]