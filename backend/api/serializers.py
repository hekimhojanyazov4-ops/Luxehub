from rest_framework import serializers
from .models import (
    PHONE_REGEX, PHONE_MESSAGE, User, Room, Reservation, Payment, Favourite, Review, NewsLetterSubscriber, RoomImage
)


from django.contrib.auth.password_validation import (
    validate_password as run_password_validators
)
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import transaction
from django.db.models import Avg
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name'
        )


class UserSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(
        write_only = True,
        required = True,
        style = {'input_type': 'password'}
    )
    class Meta:
        model = User
        fields = (
            'id',
            'created_at', 
            'updated_at',
            'is_staff',
            'is_superuser',
            'password',
            'password_confirm',
            'role',
            'email',
            'first_name',
            'last_name',
            'phone',
            'is_email_verified',
        )
        extra_kwargs = {
            'password': {
                'write_only': True,
                'required': False,
                'style': {'input_type': 'password'},
            },
            'is_staff': {'read_only': True},
            'is_superuser': {'read_only': True},
            'is_email_verified': {'read_only': True},
            'email': {'validators': []}
        }
        read_only_fields = fields

        def validate_email(self, value):
            value = value.strip().lower()
            duplicates = User.objects.filter(email__iexact=value)
            if self.instance is not None:
                duplicates = duplicates.exclude(pk=self.instance.pk)
            if duplicates.exists():
                raise serializers.ValidationError('A user with this email already exists.')
            return value

        def validate_password(self, value):
            run_password_validators(value, user = self.instance)
            return value

        def validate_role(self, value):
            request = self.context.get('request')
            if (
                self.instance is not None
                and request is not None
                and request.user.is_authenticated
                and not request.user.is_admin_role
                and value != self.instance.role
            ):
                raise serializers.ValidationError(
                    "Only administrators can change account roles."
                )
            return value


        def validate(self, attrs):
            if self.instance is None and not attrs.get('password'):
                raise serializers.ValidationError({
                    'password': "Password is required."
                })
            return attrs

        def create(self, validated_data):
            password = validated_data.pop('password')
            request = self.context.get('request')
            is_admin_request = bool(
                request and request.user.is_authenticated and request.user.is_admin_role
            )

        
            if not is_admin_request:
                validated_data['role'] = User.Role.CUSTOMER

            user = User(**validated_data) 
            user.save()
            return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        email_changed = (
            'email' in validated_data and validated_data['email'] != instance.email
        )
        role_changed = (
            'role' in validated_data and validated_data['role'] != instance.role
        )

        for field, value in validated_data.items():
            setattr(instance, field, value)

        if password:
            instance.set_password(password)
        if email_changed:
            instance.is_email_verified = False
        instance.save()  
        return instance


class RoomSerializer(serializers.ModelSerializer):  
    class RoomImageSerializer(serializers.ModelSerializer):
        room_id = serializers.UUIDField(source = 'room.id', read_only = True)
        class Meta:
            model = RoomImage
            fields = (
                'room_id',
                'image',
                'is_primary',
                'created_at',
                'updated_at',
                'id'
            )
            read_only_fields = fields
    images = RoomImageSerializer(many = True, read_only = True)
    class Meta:
        model = Room
        fields = (
            'room_type',
            'description',
            'number',
            'price_per_night',
            'capacity',
            'is_active',
        )

    def validate(self, attrs):
        instance = self.instance
        price = attrs.get('price', getattr(instance, 'price', None))
        discount = attrs.get('discount_price', getattr(instance, 'discount_price', None))
        if price is not None and discount is not None and discount > price:
            raise serializers.ValidationError({
                'discount_price': 'Discount price cannot be greater than the price.'
            })
        return attrs



class FavouriteSerializer(serializers.ModelSerializer):
    user = UserSummarySerializer(read_only = True)
    room = RoomSerializer(read_only = True)
    class Meta:
        model = Favourite
        fields = (
            'id',
            'created_at',
            'updated_at',
            'room',
            'user',
        )

class ReservationSerializer(serializers.ModelSerializer):
    user = UserSummarySerializer(read_only = True)
    room = RoomSerializer(read_only = True)
    total_price = serializers.SerializerMethodField()
    class Meta:
        model = Reservation
        fields = (
            'id',
            'created_at',
            'updated_at',
            'user',
            'room',
            'check_in',
            'check_out',
            'guests_count',
            'total_price',
            'status',
        )

class PaymentSerializer(serializers.ModelSerializer):
    reservation = ReservationSerializer(read_only = True)
    class Meta:
        model = Payment
        fields = (
            'id',
            'created_at',
            'updated_at',
            'reservation',
            'amount',
            'method',
            'status',
            'transaction_id',
            'paid_at',
        )


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSummarySerializer(read_only = True)
    room = RoomSerializer(read_only = True)
    class Meta:
        model = Review
        fields = (
            'comment',
            'user'
            'stars',
        )

    