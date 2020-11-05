from .models import RouterDetails
from rest_framework import serializers

class RouterSerializer(serializers.Serializer):
    sapid = serializers.CharField(max_length=100, allow_null=False, allow_blank=False)
    hostname = serializers.CharField(max_length=100, allow_null=False, allow_blank=False)
    loopback = serializers.CharField(max_length=100, allow_null=False, allow_blank=False)
    mac_address = serializers.CharField(max_length=100, allow_null=False, allow_blank=False)

    def create(self, validated_data):
        """
        Create and return a new `Router` instance, given the validated data.
        """
        return RouterDetails.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Router` instance, given the validated data.
        """
        instance.sapid = validated_data.get('sapid', instance.sapid)
        instance.hostname = validated_data.get('hostname', instance.hostname)
        instance.loopback = validated_data.get('loopback', instance.loopback)
        instance.mac_address = validated_data.get('mac_address', instance.mac_address)
        instance.save()
        return instance