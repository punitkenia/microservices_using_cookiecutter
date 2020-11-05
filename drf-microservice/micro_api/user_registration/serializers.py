from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100, allow_null=False, allow_blank=False)
    password = serializers.CharField(max_length=100, allow_null=False, allow_blank=False)
    email = serializers.EmailField(max_length=100, allow_null=False, allow_blank=False)

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        # remove username from being updated
        validated_data.pop('username', None)

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance