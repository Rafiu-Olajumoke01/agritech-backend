from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Farmer, Product
from .serializers import FarmerSerializer, ProductSerializer


# ------------------ Farmer Profile CRUD ------------------

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_farmer(request):
    """
    Create farmer profile for logged-in user.
    """
    if Farmer.objects.filter(user=request.user).exists():
        return Response({"error": "Farmer profile already exists."}, status=status.HTTP_400_BAD_REQUEST)
    
    data = request.data.copy()
    data['user'] = request.user.id

    serializer = FarmerSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_farmer(request):
    """
    Get logged-in farmer profile.
    """
    try:
        farmer = Farmer.objects.get(user=request.user)
    except Farmer.DoesNotExist:
        return Response({"error": "Farmer profile not found."}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = FarmerSerializer(farmer)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_farmer(request):
    """
    Update logged-in farmer profile.
    """
    try:
        farmer = Farmer.objects.get(user=request.user)
    except Farmer.DoesNotExist:
        return Response({"error": "Farmer profile not found."}, status=status.HTTP_404_NOT_FOUND)
    
    data = request.data.copy()
    data['user'] = request.user.id  # lock user to logged-in account

    serializer = FarmerSerializer(farmer, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ------------------ Farmer Product CRUD ------------------

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_product(request):
    """
    Create a product for logged-in farmer.
    """
    try:
        farmer = Farmer.objects.get(user=request.user)
    except Farmer.DoesNotExist:
        return Response({"error": "Farmer profile not found."}, status=status.HTTP_404_NOT_FOUND)

    data = request.data.copy()
    data['farmer'] = farmer.id

    serializer = ProductSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def list_products(request):
    """
    List all products (accessible to buyers).
    """
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_products(request):
    """
    Get all products posted by the logged-in farmer.
    """
    try:
        farmer = Farmer.objects.get(user=request.user)
    except Farmer.DoesNotExist:
        return Response({"error": "Farmer profile not found."}, status=status.HTTP_404_NOT_FOUND)

    products = Product.objects.filter(farmer=farmer)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_product(request, product_id):
    """
    Update a product by logged-in farmer.
    """
    try:
        product = Product.objects.get(id=product_id, farmer__user=request.user)
    except Product.DoesNotExist:
        return Response({"error": "Product not found or not owned by you."}, status=status.HTTP_404_NOT_FOUND)

    serializer = ProductSerializer(product, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_product(request, product_id):
    """
    Delete a product by logged-in farmer.
    """
    try:
        product = Product.objects.get(id=product_id, farmer__user=request.user)
    except Product.DoesNotExist:
        return Response({"error": "Product not found or not owned by you."}, status=status.HTTP_404_NOT_FOUND)

    product.delete()
    return Response({"message": "Product deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
