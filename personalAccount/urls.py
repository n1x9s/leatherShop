from django.urls import path
from . import views

app_name = 'personalAccount'

urlpatterns = [
    path('signup/', views.signup, name='signup')
]
