from django.urls import path
from . import views

app_name = 'personalAccount'

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('signin/', views.SignIn.as_view(), name='signin'),
    path('signout/', views.SignOut.as_view(), name='signout'),
    path('profile/', views.Profile.as_view(), name='profile'),
]
