from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from micro_api.router.models import RouterDetails


class APITestCaseSetup(APITestCase):
    def setUp(self):
        self.username = "sach"
        self.email = "sach@local.com"
        self.password = "123456"
        self.user = User.objects.create_user(self.username, self.email, self.password)

        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.user.auth_token))

        self.router_details = RouterDetails.objects.create(sapid='110011', hostname='110011',
                                                           loopback='127.127.127.127', mac_address='110011')
