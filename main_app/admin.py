from django.contrib import admin

from django.contrib import admin
from .models import Category, ServiceListing, ServiceRequest, Review

admin.site.register(Category)
admin.site.register(ServiceListing)
admin.site.register(ServiceRequest)
admin.site.register(Review)