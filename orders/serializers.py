from rest_framework import serializers
from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    buyer_name = serializers.CharField(source='buyer.full_name', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'buyer',
            'buyer_name',
            'product',
            'product_name',
            'product_price',
            'quantity',
            'total_price',
            'status',
            'created_at'
        ]
        read_only_fields = ['id', 'total_price', 'created_at', 'buyer_name', 'product_name', 'product_price']

    def create(self, validated_data):
        product = validated_data['product']
        quantity = validated_data.get('quantity', 1)

        validated_data['total_price'] = product.price_per_unit * quantity
       

        return super().create(validated_data)
