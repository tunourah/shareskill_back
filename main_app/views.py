from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response

# Define the home view
class Home(APIView):
  def get(self, request):
    content = {'message': 'Welcome to the capstone!'}
    return Response(content)