import logging

from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from .serializers import UserSerializer, TokenSerializer
from .models import UserInfo

logger = logging.getLogger('django')


# Create your views here.
def send_custom_mail(to_email=[], message='', subject='', from_email='sachintyagi808@gmail.com'):
    try:
        email = EmailMessage(subject, message, from_email, to_email)
        email.content_subtype = 'html'
        email.send()
    except Exception as e:
        logger.exception("send_custom_email raised an exception: " + str(e))


class UserRegistrationViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny,)

    def create(self, request):
        data = request.data
        serializer_class = UserSerializer(data=data)
        if serializer_class.is_valid():
            saved_user = serializer_class.save()

            if data['email']:
                verify_url = 'http://127.0.0.1:8000/micro_api/user/verify_email/{user_id}'.format(user_id=saved_user.id)
                email_message = '<a href="{verify_url}" target="_blank">Click to verify</a>'.format(
                    verify_url=verify_url)
                email_subject = 'Email Verification'
                email_to = data['email']
                send_custom_mail(to_email=[email_to], message=email_message, subject=email_subject)

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
        data = request.data
        queryset = self.get_queryset()
        user = get_object_or_404(queryset, pk=data['pk'])

        if data['email'] != user.email:
            verify_url = 'http://127.0.0.1:8000/micro_api/user/verify_email/{user_id}'.format(user_id=user.id)
            email_message = '<a href="{verify_url}" target="_blank">Click to verify</a>'.format(verify_url=verify_url)
            email_subject = 'Email Verification'
            email_to = data['email']
            send_custom_mail(to_email=[email_to], message=email_message, subject=email_subject)

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
        data = request.data
        user = get_object_or_404(queryset, pk=data['pk'])
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
        data = request.data
        try:
            user = User.objects.get(username=data['username'],
                                    email=data['email'])
        except:
            raise Http404

        flag = user.check_password(data['password'])
        if not flag:
            return Response({'message': 'Incorrect user details'},
                            status=status.HTTP_401_UNAUTHORIZED)

        try:
            token = Token.objects.get(user_id=user)
            # token cannot be updated. So delete the existing token
            # create new token for the user.
            token.delete()
            Token.objects.create(user=user)
            token = Token.objects.get(user_id=user)
            return Response({'username': user.username,
                             'token': token.key})
        except:
            return Response({'error': 'Unable to reset token'})


class UserEmailVerify(viewsets.ViewSet):
    permission_classes = (AllowAny,)

    def verify_email(self, request, user_id):
        user_info = UserInfo.objects.get(user_id=user_id)
        user_info.email_verify = True
        user_info.save()
        return Response({'message': 'Email verified successfully.'}, status=status.HTTP_200_OK)
