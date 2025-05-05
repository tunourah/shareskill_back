from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# Category

STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    # ---------------------------------------------------
    # ServiceListing
class ServiceListing(models.Model):
    provider = models.ForeignKey(User, related_name='service_listings', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='service_listings', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    price_description = models.CharField(max_length=100)
    location_description = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    # -------------------------------------------------
class ServiceRequest(models.Model):
    client = models.ForeignKey(User, related_name='service_requests', on_delete=models.CASCADE)
    service_listing = models.ForeignKey(ServiceListing, related_name='service_requests', on_delete=models.CASCADE)
    proposed_datetime = models.DateTimeField(blank=True, null=True)
    message = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Request {self.id} by {self.client.username}"

# ----------------------------------------------------------
class Review(models.Model):
    service_request = models.OneToOneField(ServiceRequest, related_name='review', on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review {self.id} - {self.rating} stars"
    

