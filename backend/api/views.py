from django.shortcuts import render

from .models import (
    User, Room, Review, Reservation, Payment, Favourite
)
from .serializers import (
    UserSerializer, UserSummarySerializer, PaymentSerializer, RoomSerializer, FavouriteSerializer, ReviewSerializer, ReservationSerializer
)

from rest_framework import viewsets, generics, mixins
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework import permissions
from rest_framework.pagination import PageNumberPagination



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action in ['post', 'update', 'destroy', 'put', 'patch', 'retrieve']:
            return UserSerializer
        else:
            return UserSummarySerializer

    lookup_url_kwarg = 'id'
    permission_classes = [permissions.AllowAny]
    pagination_class = PageNumberPagination
    page_size = 10
