from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .models import CustomUser
from .serializers import UserSerializer
from django.contrib.auth.hashers import make_password

# -------------------------------
# Signup / Register view
# -------------------------------
@api_view(['POST'])
@permission_classes([AllowAny])  
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "message": "User created successfully",
            "user": serializer.data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# -------------------------------
# Login view
# -------------------------------
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({"error": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)

    # Corrected: do NOT pass request into authenticate
    user = authenticate(email=email, password=password)
    
    if user is not None:
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        return Response({
            "message": "Login successful",
            "user": {
                "id": user.id,
                "full_name": user.full_name,
                "email": user.email,
                "phone": user.phone,
                "role": user.role
            },
            "tokens": {
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }
        }, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

# -------------------------------
# Get user info
# -------------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated]) 
def get_user(request, user_id):
    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)

# -------------------------------
# Update user info
# -------------------------------
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request, user_id):
    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        # Hash password if being updated
        if 'password' in serializer.validated_data:
            serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
        serializer.save()
        return Response({
            "message": "User updated successfully",
            "user": serializer.data
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# -------------------------------
# Delete user
# -------------------------------
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request, user_id):
    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    user.delete()
    return Response({"message": "User deleted successfully"}, status=status.HTTP_200_OK)
