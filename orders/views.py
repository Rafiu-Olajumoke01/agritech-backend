from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Order
from .serializers import OrderSerializer
from farmers.models import Product
from buyers.models import Buyer


# ------------------ Buyer creates an order ------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    """
    Create an order for a logged-in buyer.
    """
    try:
        buyer = Buyer.objects.get(user=request.user)
    except Buyer.DoesNotExist:
        return Response({"error": "Buyer profile not found."}, status=status.HTTP_404_NOT_FOUND)
    
    data = request.data.copy()
    data['buyer'] = buyer.id  # assign logged-in buyer
    
    serializer = OrderSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ------------------ Buyer views their orders ------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_orders(request):
    """
    Get orders for the logged-in buyer.
    """
    try:
        buyer = Buyer.objects.get(user=request.user)
    except Buyer.DoesNotExist:
        return Response({"error": "Buyer profile not found."}, status=status.HTTP_404_NOT_FOUND)
    
    orders = Order.objects.filter(buyer=buyer)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


# ------------------ Farmer views orders for their products ------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_farmer_orders(request):
    """
    Get orders for products owned by the logged-in farmer.
    """
    try:
        farmer = request.user.farmer  # assumes OneToOne relationship with User
    except:
        return Response({"error": "Farmer profile not found."}, status=status.HTTP_404_NOT_FOUND)
    
    orders = Order.objects.filter(product__farmer=farmer)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


# ------------------ Update order status (Farmer/Admin) ------------------
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_order(request, order_id):
    """
    Update order status.
    """
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = OrderSerializer(order, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ------------------ Delete order (Admin optional) ------------------
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_order(request, order_id):
    """
    Delete an order. Admin only if you want.
    """
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)
    
    order.delete()
    return Response({"message": "Order deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
