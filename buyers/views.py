from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Buyer
from .serializers import BuyerSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_buyer(request):
    """
    Create buyer profile for the logged-in user.
    """
    if Buyer.objects.filter(user=request.user).exists():
        return Response({"error": "Buyer profile already exists."}, status=status.HTTP_400_BAD_REQUEST)
    
    data = request.data.copy()
    data['user'] = request.user.id  

    serializer = BuyerSerializer(data=data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_buyer(request):
    """
    Get logged-in buyer profile.
    """
    try:
        buyer = Buyer.objects.get(user=request.user)
    except Buyer.DoesNotExist:
        return Response({"error": "Buyer profile not found."}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = BuyerSerializer(buyer)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_buyer(request):
    """
    Update buyer profile (phone, address).
    """
    try:
        buyer = Buyer.objects.get(user=request.user)
    except Buyer.DoesNotExist:
        return Response({"error": "Buyer profile not found."}, status=status.HTTP_404_NOT_FOUND)
    
    data = request.data.copy()
    data['user'] = request.user.id  
    
    serializer = BuyerSerializer(buyer, data=data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
