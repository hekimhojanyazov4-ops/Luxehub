from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    FavouriteViewSet,
    MeView,
    NewsLetterSubscriberViewSet,
    PaymentViewSet,
    RegisterView,
    ReservationViewSet,
    ReviewViewSet,
    RoomImageViewSet,
    RoomViewSet,
)

router = DefaultRouter()
router.register("rooms", RoomViewSet, basename="room")
router.register("room-images", RoomImageViewSet, basename="room-image")
router.register("reservations", ReservationViewSet, basename="reservation")
router.register("payments", PaymentViewSet, basename="payment")
router.register("favourites", FavouriteViewSet, basename="favourite")
router.register("reviews", ReviewViewSet, basename="review")
router.register("newsletter", NewsLetterSubscriberViewSet, basename="newsletter")

urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/me/", MeView.as_view(), name="me"),
    path("", include(router.urls)),
]