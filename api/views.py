from django.shortcuts import render
from shop.models import Bag
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from .permissions import IsUserAdminOrReadOnly
from .serializers import BagSerializer


class BagViewSet(viewsets.ModelViewSet):
    queryset = Bag.objects.all()
    serializer_class = BagSerializer
    permission_classes = (IsUserAdminOrReadOnly,)
