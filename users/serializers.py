from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'full_name', 'email', 'phone', 'role', 'password']
        extra_kwargs = {
            'password': {'write_only': True}  
        }

    def create(self, validated_data):
        # Hash the password before saving
        validated_data['password'] = make_password(validated_data['password'])
        user = CustomUser.objects.create(**validated_data)
        return user
