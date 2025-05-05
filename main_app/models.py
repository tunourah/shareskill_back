from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# Category
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