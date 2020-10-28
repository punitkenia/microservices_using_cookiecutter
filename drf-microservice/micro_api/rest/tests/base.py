import base64

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient, APITestCase

from micro_api.rest.models import RouterDetails

class BaseTestCase(TestCase):
    """A base test case."""

    def setUp(self):
        self.client = APIClient()
        self.user = \
            User.objects.create(username="my_user", password="my_passwd")

    def tearDown(self):
        pass

    def basics_auth_get(self, url, username, password,
                        data=None, content_type='application/json'):
        valid_credentials = base64.b64encode(
            bytes(username + ":" + password, 'ascii')).decode('ascii')
        return self.client.get(
            url,
            headers={
                'Authorization': 'Basic ' + valid_credentials
            },
            content_type=content_type,
            data=data
        )

    def basics_auth_post(self, url, username, password, data, format='json'):
        valid_credentials = base64.b64encode(
            bytes(username + ":" + password, 'ascii')).decode('ascii')
        # see http://www.django-rest-framework.org/api-guide/testing/
        return self.client.post(
            url,
            headers={
                'Authorization': 'Basic ' + valid_credentials
            },
            format=format,
            data=data
        )

    def token_auth_get(self, url, token,
                       data=None, content_type='application/json'):
        return self.client.get(
            url,
            headers={
                'Authorization': 'Token ' + token
            },
            content_type=content_type,
            data=data
        )

    def token_auth_post(self, url, token, data, format='json'):
        return self.client.post(
            url,
            headers={
                'Authorization': 'Token ' + token
            },
            format=format,
            data=data
        )


class APITestCaseSetup(APITestCase):
    def setUp(self):
        self.username = "sach"
        self.email = "sach@local.com"
        self.password = "123456"
        self.user = User.objects.create_user(self.username, self.email, self.password)

        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.user.auth_token))

        self.router_details = RouterDetails.objects.create(sapid='110011', hostname='110011',
                                                           loopback='127.127.127.127', mac_address='110011')
