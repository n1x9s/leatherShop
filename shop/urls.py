from django.urls import path

from . import views


app_name = 'shop'
urlpatterns = [
    path("", views.Index.as_view(), name='index'),
    path('detail/<int:id_bag>', views.Detail.as_view(), name='detail'),
]
