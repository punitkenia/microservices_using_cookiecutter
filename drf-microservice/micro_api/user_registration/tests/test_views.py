from ddt import ddt, data
from django.urls import reverse
from rest_framework import status

from .base import UserApiTestSetup
from micro_api.user_registration.views import UserViewSet


@ddt
class UserViewSetTest(UserApiTestSetup):

    def test_get_queryset(self):
        user_registration = UserViewSet()
        result = user_registration.get_queryset()
        result_username = [obj.username for obj in result]
        self.assertTrue(self.username in result_username)

    def test_list(self):
        response = self.client.get(reverse('list-user'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @data(10, 11, 12, 13, 14)
    def test_retrieve(self, user_id):
        response = self.client.get(reverse('user-details', kwargs={'pk': self.user.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_not_valid = self.client.get(reverse('user-details', kwargs={'pk': user_id}))
        self.assertEqual(response_not_valid.status_code, status.HTTP_404_NOT_FOUND)

    @data(10)
    def test_destroy(self, user_id):
        response = self.client.post(reverse('user-delete'), data={'pk': self.user.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response_not_found = self.client.post(reverse('user-delete'), data={'pk': user_id}, format='json')
        self.assertEqual(response_not_found.status_code, status.HTTP_404_NOT_FOUND)
