from rest_framework import serializers
from .models import Farmer, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'farmer', 'crop_type', 'quantity_with_unit', 'price_per_unit', 'created_at']
        read_only_fields = ['id', 'created_at']


class FarmerSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Farmer
        fields = ['id', 'user', 'farm_name', 'farm_location', 'created_at', 'products']
        read_only_fields = ['id', 'created_at', 'products']
