from rest_framework import generics, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Favourite, NewsLetterSubscriber, Payment, Reservation, Review, Room, RoomImage
from .permissions import IsAdminOrManager, IsAdminOrManagerOrReadOnly, IsOwnerOrAdminOrManager
from .serializers import (
    FavouriteSerializer,
    NewsLetterSubscriberSerializer,
    PaymentSerializer,
    RegisterSerializer,
    ReservationSerializer,
    ReservationStatusUpdateSerializer,
    ReviewSerializer,
    RoomAvailabilitySerializer,
    RoomImageSerializer,
    RoomSerializer,
    UserSerializer,
)


# ---------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------

class RegisterView(generics.CreateAPIView):
    """POST /auth/register/ — public signup."""

    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class MeView(generics.RetrieveUpdateAPIView):
    """GET/PATCH /auth/me/ — the logged-in user's own profile."""

    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


# ---------------------------------------------------------------------
# Rooms
# ---------------------------------------------------------------------

class RoomViewSet(viewsets.ModelViewSet):
    """
    Public read access; only ADMIN/MANAGER can create, update or delete.
    Supports ?room_type=, ?min_price=, ?max_price=, ?guests= filters.
    """

    serializer_class = RoomSerializer
    permission_classes = [IsAdminOrManagerOrReadOnly]

    def get_queryset(self):
        qs = Room.objects.all().prefetch_related("images", "reviews")

        user = self.request.user
        staff = bool(user and user.is_authenticated and user.is_staff_role)
        if not staff:
            qs = qs.filter(is_active=True)

        params = self.request.query_params
        room_type = params.get("room_type")
        if room_type:
            qs = qs.filter(room_type=room_type)

        min_price = params.get("min_price")
        if min_price:
            qs = qs.filter(price_per_night__gte=min_price)

        max_price = params.get("max_price")
        if max_price:
            qs = qs.filter(price_per_night__lte=max_price)

        guests = params.get("guests")
        if guests:
            qs = qs.filter(capacity__gte=guests)

        return qs

    @action(detail=True, methods=["post"], permission_classes=[permissions.AllowAny])
    def check_availability(self, request, pk=None):
        """POST /rooms/{id}/check_availability/ {check_in, check_out}"""
        room = self.get_object()
        serializer = RoomAvailabilitySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        available = room.is_available_for(
            serializer.validated_data["check_in"],
            serializer.validated_data["check_out"],
        )
        return Response({"available": available})


class RoomImageViewSet(viewsets.ModelViewSet):
    """ADMIN/MANAGER only. Supports ?room=<id> filter."""

    serializer_class = RoomImageSerializer
    permission_classes = [IsAdminOrManager]

    def get_queryset(self):
        qs = RoomImage.objects.select_related("room")
        room_id = self.request.query_params.get("room")
        if room_id:
            qs = qs.filter(room_id=room_id)
        return qs


# ---------------------------------------------------------------------
# Reservations
# ---------------------------------------------------------------------

class ReservationViewSet(viewsets.ModelViewSet):
    """
    Customers see and manage only their own reservations.
    ADMIN/MANAGER see and manage all of them.
    """

    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdminOrManager]

    def get_queryset(self):
        user = self.request.user
        qs = Reservation.objects.select_related("room", "user")
        if user.is_staff_role:
            return qs
        return qs.filter(user=user)

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        """POST /reservations/{id}/cancel/ — owner or staff can cancel."""
        reservation = self.get_object()
        if reservation.status not in (Reservation.Status.PENDING, Reservation.Status.CONFIRMED):
            return Response(
                {"detail": "Bu bron ýatyrylyp bilinmez."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        reservation.status = Reservation.Status.CANCELLED
        reservation.save(update_fields=["status", "updated_at"])
        return Response(ReservationSerializer(reservation).data)

    @action(
        detail=True,
        methods=["patch"],
        permission_classes=[permissions.IsAuthenticated, IsAdminOrManager],
    )
    def set_status(self, request, pk=None):
        """PATCH /reservations/{id}/set_status/ {status} — staff only."""
        reservation = self.get_object()
        serializer = ReservationStatusUpdateSerializer(reservation, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(ReservationSerializer(reservation).data)


# ---------------------------------------------------------------------
# Payments
# ---------------------------------------------------------------------

class PaymentViewSet(viewsets.ModelViewSet):
    """
    Customers can view (read-only) payments tied to their own reservations.
    Only ADMIN/MANAGER can create/update/delete payment records.
    """

    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = Payment.objects.select_related("reservation", "reservation__user")
        if user.is_staff_role:
            return qs
        return qs.filter(reservation__user=user)

    def get_permissions(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return [permissions.IsAuthenticated(), IsAdminOrManager()]
        return super().get_permissions()


# ---------------------------------------------------------------------
# Favourites
# ---------------------------------------------------------------------

class FavouriteViewSet(viewsets.ModelViewSet):
    """A user's own saved/favourited rooms."""

    serializer_class = FavouriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Favourite.objects.filter(user=self.request.user).select_related("room")


# ---------------------------------------------------------------------
# Reviews
# ---------------------------------------------------------------------

class ReviewViewSet(viewsets.ModelViewSet):
    """
    Public read access. Any authenticated customer can create a review;
    only the review's author or staff can edit/delete it.
    Supports ?room=<id> filter.
    """

    serializer_class = ReviewSerializer
    permission_classes = [IsAdminOrManagerOrReadOnly]

    def get_queryset(self):
        qs = Review.objects.select_related("user", "room")
        room_id = self.request.query_params.get("room")
        if room_id:
            qs = qs.filter(room_id=room_id)
        return qs

    def get_permissions(self):
        if self.action == "create":
            return [permissions.IsAuthenticated()]
        if self.action in ("update", "partial_update", "destroy"):
            return [permissions.IsAuthenticated(), IsOwnerOrAdminOrManager()]
        return super().get_permissions()


# ---------------------------------------------------------------------
# Newsletter
# ---------------------------------------------------------------------

class NewsLetterSubscriberViewSet(viewsets.ModelViewSet):
    """Anyone can subscribe (create); only staff can list/manage."""

    queryset = NewsLetterSubscriber.objects.all()
    serializer_class = NewsLetterSubscriberSerializer

    def get_permissions(self):
        if self.action == "create":
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), IsAdminOrManager()]