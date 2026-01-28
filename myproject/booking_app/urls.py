from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import (
    UserProfileListAPIView,UserProfileDetailAPIView,
    RoomListAPIView,RoomDetailAPIView,
    ReviewCreateAPIView,
    BookingViewSet, CityListAPIView,
    CityDetailAPIView, HotelListAPIView, HotelDetailAPIView,
    ReviewEditAPIView, HotelViewSet, RegisterView, LoginView, LogoutView
)

router = SimpleRouter()
router.register(r'bookings', BookingViewSet),
router.register(r'hotel_create', HotelViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('city/', CityListAPIView.as_view(), name='city_list'),
    path('city/<int:pk>/', CityDetailAPIView.as_view(), name='city_detail'),
    path('hotels/', HotelListAPIView.as_view(), name='hotel_list'),
    path('hotels/<int:pk>/', HotelDetailAPIView.as_view(), name='hotel_detail'),
    path('rooms/',RoomListAPIView.as_view(),name='rooms_list'),
    path('rooms/<int:pk>/',RoomDetailAPIView.as_view(),name='room_detail'),
    path('userprofile/',UserProfileListAPIView.as_view(),name="userprofile_list"),
    path('userprofile/<int:pk>/',UserProfileDetailAPIView.as_view(),name='userprofile_detail'),
    path('reviews/', ReviewCreateAPIView.as_view(), name='create_review'),
    path('reviews/<int:pk>/', ReviewEditAPIView.as_view(), name='edit_review'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout')
]
