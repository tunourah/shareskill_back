from django.test import TestCase
from django.contrib.auth.models import User
from main_app.models import Category, ServiceListing, ServiceRequest, Review
from datetime import datetime

class ModelsTest(TestCase):
    def setUp(self):
        # Create a test user
        self.provider = User.objects.create_user(username='provider', password='testpass')
        self.client_user = User.objects.create_user(username='client', password='testpass')

        # Create a category
        self.category = Category.objects.create(name='Tutoring', description='Help with schoolwork')

        # Create a service listing
        self.service = ServiceListing.objects.create(
            provider=self.provider,
            category=self.category,
            title='Math Tutoring',
            description='I help with math homework.',
            price_description='50 SAR/hour',
            location_description='Riyadh',
            is_active=True
        )

        # Create a service request
        self.request = ServiceRequest.objects.create(
            client=self.client_user,
            service_listing=self.service,
            proposed_datetime=datetime(2025, 6, 1, 17, 0),
            message='Can you help with algebra?',
            status='completed'
        )

        # Create a review
        self.review = Review.objects.create(
            service_request=self.request,
            reviewer=self.client_user,
            rating=5,
            comment='Very helpful!'
        )

    # Test string representations
    def test_user_str(self):
        self.assertEqual(str(self.provider), 'provider')

    def test_category_str(self):
        self.assertEqual(str(self.category), 'Tutoring')

    def test_service_listing_str(self):
        self.assertEqual(str(self.service), 'Math Tutoring')

    def test_service_request_str(self):
        self.assertIn('Request', str(self.request))
        self.assertIn('client', str(self.request))

    def test_review_str(self):
        self.assertIn('Review', str(self.review))
        self.assertIn('stars', str(self.review))

    # Relationship Tests
    def test_service_provider_relationship(self):
        self.assertEqual(self.service.provider.username, 'provider')

    def test_service_category_relationship(self):
        self.assertEqual(self.service.category.name, 'Tutoring')

    def test_request_client_relationship(self):
        self.assertEqual(self.request.client.username, 'client')

    def test_request_service_relationship(self):
        self.assertEqual(self.request.service_listing.title, 'Math Tutoring')

    def test_review_request_relationship(self):
        self.assertEqual(self.review.service_request, self.request)
        self.assertEqual(self.review.reviewer.username, 'client')

    # Cascade deletion tests
    def test_deleting_service_deletes_requests(self):
        self.assertEqual(ServiceRequest.objects.count(), 1)
        self.service.delete()
        self.assertEqual(ServiceRequest.objects.count(), 0)

    def test_deleting_request_deletes_review(self):
        self.assertEqual(Review.objects.count(), 1)
        self.request.delete()
        self.assertEqual(Review.objects.count(), 0)

    def test_deleting_user_deletes_services(self):
        self.assertEqual(ServiceListing.objects.count(), 1)
        self.provider.delete()
        self.assertEqual(ServiceListing.objects.count(), 0)
