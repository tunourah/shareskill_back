# import Home view from the views file
from .views import Home
from django.urls import path
from .views import CreateUserView , LoginView

urlpatterns = [
  path('', Home.as_view(), name='home'),
  path('users/signup/', CreateUserView.as_view(), name='signup'),
  path('users/login/', LoginView.as_view(), name='login'),

]