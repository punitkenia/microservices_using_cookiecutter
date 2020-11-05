from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from .serializers import UserSerializer

# Create your views here.
class UserRegistrationViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny,)

    def create(self, request):
        data = request.data
        serializer_class = UserSerializer(data=data)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(serializer_class.data)
        return Response(serializer_class.errors)


class UserViewSet(viewsets.ViewSet):

    def get_queryset(self):
        return User.objects.filter(is_active=True)

    def list(self, request, format=None):
        queryset = self.get_queryset()
        serializer_class = UserSerializer(queryset, many=True)
        return Response(serializer_class.data)

    def update(self, request, pk, format=None):
        data = request.data
        queryset = self.get_queryset()
        user = get_object_or_404(queryset, pk=pk)
        serializer_class = UserSerializer(user, data=data)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(serializer_class.data)
        return Response(serializer_class.errors)

    def retrieve(self, request, pk, format=None):
        queryset = self.get_queryset()
        user = get_object_or_404(queryset, pk=pk)
        serializer_class = UserSerializer(user)
        return Response(serializer_class.data)

    def destroy(self, request, pk, format=None):
        queryset = self.get_queryset()
        user = get_object_or_404(queryset, pk=pk)
        user.is_active = False
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)