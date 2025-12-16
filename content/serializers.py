from rest_framework import serializers
from .models import Content

class ContentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.full_name', read_only=True)

    class Meta:
        model = Content
        fields = [
            'id',
            'title',
            'body',
            'type',
            'author',
            'author_name',
            'cover_image',
            'video_url',
            'is_published',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'author_name', 'created_at', 'updated_at']
