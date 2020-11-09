from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from .serializers import UserSerializer, TokenSerializer

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

    def update(self, request, format=None):
        data = request.data.dict()
        queryset = self.get_queryset()
        user = get_object_or_404(queryset, pk=data['pk'])
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

    def destroy(self, request, format=None):
        queryset = self.get_queryset()
        data = request.data.dict()
        user = get_object_or_404(queryset, pk=data['pk'])
        user.is_active = False
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserToken(viewsets.ViewSet):

    def get_queryset(self):
        return User.objects.filter(is_active=True)

    def retrieve(self, request, pk, format=None):
        queryset = self.get_queryset()
        user = get_object_or_404(queryset, pk=pk)
        token = Token.objects.get(user_id=user)
        serializer_class = TokenSerializer(token)
        return Response(serializer_class.data)

    def update(self, request, format=None):
        data = request.data.dict()
        try:
            user = User.objects.get(username=data['username'],
                                    email=data['email'])
        except:
            raise Http404

        flag = user.check_password(data['password'])
        if not flag:
            return Response({'message' : 'Incorrect user details'},
                            status=status.HTTP_401_UNAUTHORIZED)

        try:
            token = Token.objects.get(user_id=user)
            # token cannot be updated. So delete the existing token
            # create new token for the user.
            token.delete()
            Token.objects.create(user=user)
            token = Token.objects.get(user_id=user)
            return Response({'username' : user.username,
                             'token' : token.key})
        except:
            return Response({'error' : 'Unable to reset token'})
