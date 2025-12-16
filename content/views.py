from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status

from .models import Content
from .serializers import ContentSerializer


# ----------------------
# Create content (Admin only)
# ----------------------
@api_view(['POST'])
@permission_classes([IsAdminUser])
def create_content(request):
    """
    Admin can create new content. Optional fields (cover_image, video_url) can be empty.
    """
    data = request.data.copy()
    data['author'] = request.user.id

    serializer = ContentSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ----------------------
# Get all published content (Everyone)
# ----------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_content(request):
    """
    List all published content for buyers/farmers.
    """
    contents = Content.objects.filter(is_published=True).order_by('-created_at')
    serializer = ContentSerializer(contents, many=True)
    return Response(serializer.data)


# ----------------------
# Get single content
# ----------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_content(request, content_id):
    """
    Retrieve a single content item by ID.
    """
    try:
        content = Content.objects.get(id=content_id)
    except Content.DoesNotExist:
        return Response({"error": "Content not found."}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = ContentSerializer(content)
    return Response(serializer.data)


# ----------------------
# Update content (Admin only)
# ----------------------
@api_view(['PUT'])
@permission_classes([IsAdminUser])
def update_content(request, content_id):
    """
    Admin can update content fields (title, body, type, cover_image, video_url, is_published).
    """
    try:
        content = Content.objects.get(id=content_id)
    except Content.DoesNotExist:
        return Response({"error": "Content not found."}, status=status.HTTP_404_NOT_FOUND)
    
    data = request.data.copy()
    serializer = ContentSerializer(content, data=data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ----------------------
# Delete content (Admin only)
# ----------------------
@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_content(request, content_id):
    """
    Admin can delete content.
    """
    try:
        content = Content.objects.get(id=content_id)
    except Content.DoesNotExist:
        return Response({"error": "Content not found."}, status=status.HTTP_404_NOT_FOUND)
    
    content.delete()
    return Response({"message": "Content deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

