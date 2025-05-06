from django.contrib.auth.models import User
from rest_framework import serializers
 
from django.db.models import Avg
from .models import Review
from .models import Category, ServiceListing, ServiceRequest, Review

class UserSerializer(serializers.ModelSerializer):
    # Add a password field, make it write-only
    # prevents allowing 'read' capabilities (returning the password via api response)
    password = serializers.CharField(write_only=True)  

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']  
        )
      
        return user



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ServiceListingSerializer(serializers.ModelSerializer):
    provider_username = serializers.ReadOnlyField(source='provider.username')
    category_name     = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = ServiceListing
        # still include all the other fields…
        fields = '__all__'
        # …but make provider read-only so it's not required in the POST body
        extra_kwargs = {
            'provider': {'read_only': True},
        }

class ServiceRequestSerializer(serializers.ModelSerializer):
    client = serializers.ReadOnlyField(source='client.username')
    service_title = serializers.ReadOnlyField(source='service_listing.title')

    class Meta:
        model = ServiceRequest
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    reviewer = serializers.ReadOnlyField(source='reviewer.username')
    class Meta:
        model = Review
        fields = '__all__'
class ServiceListingDetailSerializer(serializers.ModelSerializer):
    provider     = UserSerializer(read_only=True)
    category     = CategorySerializer(read_only=True)
    avg_rating   = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()

    class Meta:
        model = ServiceListing
        fields = [
            'id',
            'provider',
            'category',
            'title',
            'description',
            'price_description',
            'location_description',
            'is_active',
            'created_at',
            'updated_at',
            # our extra two:
            'avg_rating',
            'review_count',
        ]

    def get_avg_rating(self, obj):
        qs = Review.objects.filter(
            service_request__service_listing=obj,
            service_request__status='completed'
        )
        agg = qs.aggregate(avg=Avg('rating'))
        return agg['avg'] or 0

    def get_review_count(self, obj):
        return Review.objects.filter(
            service_request__service_listing=obj,
            service_request__status='completed'
        ).count()
