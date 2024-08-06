from rest_framework import serializers

from shop.models import Bag


class BagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bag
        fields = '__all__'
