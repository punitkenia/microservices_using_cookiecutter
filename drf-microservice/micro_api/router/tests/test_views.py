from django.urls import reverse
from rest_framework import status
from ddt import ddt, data, unpack

from .base import APITestCaseSetup
from micro_api.router.views import RouterViewSet


@ddt
class TestRouterViewSetViews(APITestCaseSetup):

    def test_get_queryset(self):
        router_viewset = RouterViewSet()
        result = router_viewset.get_queryset()
        result_sapid = [obj.sapid for obj in result]
        self.assertTrue(self.router_details.sapid in result_sapid)

    def test_list_get(self):
        url = reverse('router-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @data(10, 11, 12, 13)
    def test_retrieve(self, router_id):
        response = self.client.get(reverse('router-detail', kwargs={'pk': self.router_details.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_not_valid = self.client.get(reverse('router-detail', kwargs={'pk': router_id}))
        self.assertEqual(response_not_valid.status_code, status.HTTP_404_NOT_FOUND)

    @data(['110012', 'hostname1', '12.23.34.45', 'M110012'],
          ['110013', 'hostname2', '23.34.45.56', 'M110013'])
    @unpack
    def test_create(self, sapid, hostname, loopback, mac_address):
        router_data = {
            'sapid': sapid,
            'hostname': hostname,
            'loopback': loopback,
            'mac_address': mac_address,
        }

        response = self.client.post(reverse('router-list'), data=router_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        router_data_not_valid = {
            'sapid': sapid,
            'hostname': '',
            'loopback': loopback,
            'mac_address': mac_address,
        }

        response_not_valid = self.client.post(reverse('router-list'), data=router_data_not_valid, format='json')
        self.assertEqual(response_not_valid.status_code, status.HTTP_400_BAD_REQUEST)

    @data({'sapid': '110012', 'hostname': 'hostname1', 'loopback': '12.23.34.45', 'mac_address': 'M110012',
           'router_id': 10},
          {'sapid': '110013', 'hostname': 'hostname2', 'loopback': '23.34.45.56', 'mac_address': 'M110013',
           'router_id': 11})
    @unpack
    def test_update(self, sapid, hostname, loopback, mac_address, router_id):
        """router_id parameter will be used for 'not found case only' """

        # Positive test case
        router_data = {
            'id': self.router_details.id,
            'sapid': sapid,
            'hostname': hostname,
            'loopback': loopback,
            'mac_address': mac_address,
        }

        response = self.client.post(reverse('router-update'), data=router_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Test Case: Where record needs to be updated, not found
        router_data_not_found = {
            'id': router_id,
            'sapid': sapid,
            'hostname': hostname,
            'loopback': loopback,
            'mac_address': mac_address,
        }

        response_not_found = self.client.post(reverse('router-update'), data=router_data_not_found, format='json')
        self.assertEqual(response_not_found.status_code, status.HTTP_404_NOT_FOUND)

        # Test Case: Where data is not validated
        router_data_not_valid = {
            'id': self.router_details.id,
            'sapid': sapid,
            'hostname': '',
            'loopback': loopback,
            'mac_address': mac_address,
        }

        response_not_valid = self.client.post(reverse('router-update'), data=router_data_not_valid, format='json')
        self.assertEqual(response_not_valid.status_code, status.HTTP_400_BAD_REQUEST)

    @data(10)
    def test_destroy(self, router_id):
        response = self.client.post(reverse('remove-router'), data={'id': self.router_details.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response_not_found = self.client.post(reverse('remove-router'), data={'id': router_id}, format='json')
        self.assertEqual(response_not_found.status_code, status.HTTP_404_NOT_FOUND)
