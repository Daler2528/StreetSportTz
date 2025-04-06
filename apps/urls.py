from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.views import StadiumCreateAPIView, StadiumDeleteAPIView, StadiumListAPIView, StadiumDetailAPIView, \
    StadiumCountView, MyStadiumStatsView, RegisterAPIView, LoginAPIView, StadiumBookingAPIView, MyBookingsAPIView, \
    BookingUpdateAPIView

urlpatterns = [
# Stadium
    path('stadium-create' , StadiumCreateAPIView.as_view()),
    path('stadium-delete/<int:pk>' , StadiumDeleteAPIView.as_view()),
    path('stadium-list' , StadiumListAPIView.as_view()),
    path('stadium-detail/<int:pk>' , StadiumDetailAPIView.as_view()),

    path('stadium-count' , StadiumCountView.as_view()),

    path('api/my-stadium-stats/', MyStadiumStatsView.as_view(), name='my-stadium-stats'),

    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('api/book/', StadiumBookingAPIView.as_view(), name='stadium-booking'),
    path('booking', MyBookingsAPIView.as_view()),
    path('booking-update/<int:pk>', BookingUpdateAPIView.as_view()),


]