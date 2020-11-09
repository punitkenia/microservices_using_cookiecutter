import datetime

from django.contrib.auth.models import User
from rest_framework import serializers
# from .models import CustomUser

class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100, allow_null=False, allow_blank=False)
    password = serializers.CharField(max_length=100, allow_null=False, allow_blank=False)
    email = serializers.EmailField(max_length=100, allow_null=False, allow_blank=False)

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(
            username = validated_data['username'],
            email = validated_data['email']
        )
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        # remove username and password from being updated
        validated_data.pop('username', None)
        validated_data.pop('password', None)

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        instance.save()
        return instance


class TokenSerializer(serializers.Serializer):
    key = serializers.CharField(max_length=100, allow_null=False, allow_blank=False)
    user_id = serializers.IntegerField(allow_null=False)