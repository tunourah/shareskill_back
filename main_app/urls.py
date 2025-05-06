# main_app/urls.py

from django.urls import path
from .views import (
    Home,
    CreateUserView,
    LoginView,
    VerifyUserView,                
    CategoryListCreateView,
    CategoryDetailView,
    ServiceListingListCreateView,
    ServiceListingDetailView,
    ServiceRequestListCreateView,
    ServiceRequestDetailView,
    ReviewListCreateView,
    ReviewDetailView,
)

urlpatterns = [
    # check / root
    path('', Home.as_view(), name='home'),

    # Auth
    path('users/signup/', CreateUserView.as_view(), name='signup'),
    path('users/login/',  LoginView.as_view(),  name='login'),
    path('users/verify/', VerifyUserView.as_view(), name='verify-user'),

    # Categories (admin only)
    path('categories/',         CategoryListCreateView.as_view(),   name='category-list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(),     name='category-detail'),

    # Service Listings
    path('service-listings/',         ServiceListingListCreateView.as_view(), name='listing-list'),
    path('service-listings/<int:pk>/', ServiceListingDetailView.as_view(),   name='listing-detail'),

    # Service Requests
    path('service-requests/',         ServiceRequestListCreateView.as_view(), name='request-list'),
    path('service-requests/<int:pk>/', ServiceRequestDetailView.as_view(),   name='request-detail'),

    # Reviews
    path('reviews/',         ReviewListCreateView.as_view(),   name='review-list'),
    path('reviews/<int:pk>/', ReviewDetailView.as_view(),     name='review-detail'),
]
