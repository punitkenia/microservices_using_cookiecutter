from django.contrib.auth.models import User
from rest_framework.test import APITestCase


class UserApiTestSetup(APITestCase):
    def setUp(self):
        self.username = "sach"
        self.email = "sach@local.com"
        self.password = "123456"
        self.user = User.objects.create_user(self.username, self.email, self.password)

        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.user.auth_token))
