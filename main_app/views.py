from django.shortcuts import render
from rest_framework import generics, status
from rest_framework import viewsets, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .serializers import UserSerializer
from django.contrib.auth import authenticate
from django.db.models import Q
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import generics, status, filters
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated, IsAdminUser , AllowAny , IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from .models import Category, ServiceListing, ServiceRequest, Review
from .serializers import CategorySerializer, ServiceListingSerializer, ServiceRequestSerializer, ReviewSerializer , ServiceListingDetailSerializer 
from rest_framework.parsers import MultiPartParser, FormParser

class Home(APIView):
  def get(self, request):
    content = {'message': 'Welcome to the capstone!'}
    return Response(content)
  


# User Registration
class CreateUserView(generics.CreateAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer

  def create(self, request, *args, **kwargs):
    try:
      response = super().create(request, *args, **kwargs)
      user = User.objects.get(username=response.data['username'])
      refresh = RefreshToken.for_user(user)
      content = {'refresh': str(refresh), 'access': str(refresh.access_token), 'user': response.data }
      return Response(content, status=status.HTTP_200_OK)
    except (ValidationError, IntegrityError) as err:
      return Response({ 'error': str(err)}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):

  def post(self, request):
    try:
      username = request.data.get('username')
      password = request.data.get('password')
      user = authenticate(username=username, password=password)
      if user:
        refresh = RefreshToken.for_user(user)
        content = {'refresh': str(refresh), 'access': str(refresh.access_token),'user': UserSerializer(user).data}
        return Response(content, status=status.HTTP_200_OK)
      return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as err:
      return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class VerifyUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            # re-issue fresh tokens
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            }, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({
                "detail": "Unexpected error occurred.",
                "error": str(err)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# --- Category Endpoints (Admin Only) ---

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny] 
    


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]


# --- ServiceListing Endpoints ---

class ServiceListingListCreateView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]  # ✅ Added to fix 404 due to blocked unauth access
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_active', 'location_description']
    search_fields = ['title', 'description', 'location_description']
    ordering_fields = ['created_at', 'title']
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        qs = ServiceListing.objects.select_related('category', 'provider')
        provider_flag = self.request.query_params.get('provider')
        if provider_flag == 'current':
            if not self.request.user.is_authenticated:
                raise PermissionDenied("Authentication required to view your listings.")
            qs = qs.filter(provider=self.request.user)
        else:
            qs = qs.filter(is_active=True)

        # additional filters
        if search := self.request.query_params.get('search'):
            qs = qs.filter(title__icontains=search)
        if cat := self.request.query_params.get('category'):
            qs = qs.filter(category_id=cat)
        if loc := self.request.query_params.get('location'):
            qs = qs.filter(location_description__icontains=loc)

        return qs

    def get_serializer_class(self):
        return ServiceListingSerializer

    def perform_create(self, serializer):
        serializer.save(provider=self.request.user)
        


class ServiceListingDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ServiceListing.objects.select_related('category', 'provider')
    serializer_class = ServiceListingDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        if serializer.instance.provider != self.request.user:
            raise PermissionDenied("You can only update your own listings.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.provider != self.request.user:
            raise PermissionDenied("You can only delete your own listings.")
        instance.delete()
    def get_serializer_context(self):
        return {'request': self.request}


# --- ServiceRequest Endpoints ---

class ServiceRequestListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ServiceRequestSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'service_listing']
    ordering_fields = ['created_at']

    def get_queryset(self):
        qs = ServiceRequest.objects.select_related(
            'client', 'service_listing', 'service_listing__provider'
        )
        client_flag = self.request.query_params.get('client')
        provider_flag = self.request.query_params.get('provider')

        if client_flag == 'current':
            qs = qs.filter(client=self.request.user)
        if provider_flag == 'current':
            qs = qs.filter(service_listing__provider=self.request.user)
        if status_val := self.request.query_params.get('status'):
            qs = qs.filter(status__iexact=status_val)

        return qs

    def perform_create(self, serializer):
        serializer.save(client=self.request.user)


class ServiceRequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ServiceRequest.objects.select_related(
        'client', 'service_listing', 'service_listing__provider'
    )
    serializer_class = ServiceRequestSerializer
    # permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        instance = serializer.instance
        user = self.request.user

        # Only provider can change status (client may cancel)
        if 'status' in self.request.data:
            if instance.service_listing.provider != user:
                if not (instance.client == user and self.request.data['status'] == 'cancelled'):
                    raise PermissionDenied("Only provider may update status.")
        serializer.save()

    def perform_destroy(self, instance):
        # allow client to delete their own request
        if instance.client != self.request.user:
            raise PermissionDenied("You can only cancel your own request.")
        instance.delete()


# --- Review Endpoints ---

class ReviewListCreateView(generics.ListCreateAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['service_request__service_listing']
    ordering_fields = ['created_at', 'rating']

    def get_queryset(self):
        qs = Review.objects.select_related(
            'reviewer', 'service_request', 'service_request__service_listing'
        )
        if sl := self.request.query_params.get('service_listing'):
            qs = qs.filter(service_request__service_listing_id=sl)
        return qs

    def perform_create(self, serializer):
        sr = ServiceRequest.objects.get(pk=self.request.data.get('service_request'))
        if sr.client != self.request.user:
            raise PermissionDenied("You can only review requests you made.")
        if sr.status != 'completed':
            raise ValidationError("Can only review completed requests.")
        serializer.save(reviewer=self.request.user)


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.select_related('reviewer', 'service_request')
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        if serializer.instance.reviewer != self.request.user:
            raise PermissionDenied("You can only update your own reviews.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.reviewer != self.request.user:
            raise PermissionDenied("You can only delete your own reviews.")
        instance.delete()