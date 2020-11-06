from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from .serializers import UserSerializer, UserUpdateLogSerializer
from .models import UserUpdateLog


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

        if user:
            user_data = {
                'user_id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'username': user.username,
                'password': user.password,
            }
            serializer_user_update_log = UserUpdateLogSerializer(data=user_data)
            if serializer_user_update_log.is_valid():
                serializer_user_update_log.save()

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

    def update_role(self, request, pk):
        data = request.data
        queryset = self.get_queryset()
        user = get_object_or_404(queryset, pk=pk)

        if data['superuser'] == '1':
            user.is_superuser = True
            user.is_staff = True
        else:
            user.is_superuser = False
            user.is_staff = True

        user.save()
        return Response({'message': 'Role updated successfully.'}, status=status.HTTP_200_OK)

    def profile_history(self, request, user_id):
        history = UserUpdateLog.objects.filter(user_id= user_id).order_by('-date_joined')[:10]
        serializer_user_update_log = UserUpdateLogSerializer(history, many=True)
        return Response(serializer_user_update_log.data)
