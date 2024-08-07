from rest_framework import viewsets

from shop.models import Bag
from .permissions import IsUserAdminOrReadOnly
from .serializers import BagSerializer


class BagViewSet(viewsets.ModelViewSet):
    queryset = Bag.objects.all()
    serializer_class = BagSerializer
    permission_classes = [IsUserAdminOrReadOnly]
