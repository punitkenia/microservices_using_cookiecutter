import json

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from docs.version import __version__
from micro_api.rest.serializers import FileToFilesystemSerializer, RouterSerializer
from micro_api.rest.models import RouterDetails


"""
Official drf doc here:
https://www.django-rest-framework.org/api-guide/requests/#authenticators
"""


@api_view(['GET'])
def status_api(request):
    """
    For Icinga2 or Nagios. Function based.
    Return 'status': 'OK' and the current version running.
    """
    if request.method == 'GET':
        return JsonResponse({
            'status': 'OK',
            'version': __version__
        }, status=200)


class Icinga2API(APIView):
    """
    For Icinga2 or Nagios. Class based.
    Return 'status': 'OK' and the current version running.
    """
    def get(self, request):
        return Response({
            'status': 'OK',
            'version': __version__
        }, status=200)


class FileAPI(APIView):
    """
    Example API to push a json image on the server and get it by a key.
    """
    # def delete(self, request):
    #     """
    #     Required that the client is authenticated,
    #     This method delete a file on the disk (NotImplemented)
    #     :param request: the key corresponding to that file.
    #     :return: status
    #     """
    #     raise NotImplemented()

    def get(self, request):
        """
        Required that the client is authenticated,
        This method load a file from the disk to the json send it in the
        response
        :param request: the key corresponding to that file.
        :return: the file in json Base64 format
        """
        # http://www.django-rest-framework.org/api-guide/requests/#query_params
        if 'name' not in request.query_params \
                or not request.query_params['name']:
            return Response({'error': 'file Not found'}, status=422)
        else:
            name = request.query_params['name']

        with open(settings.PATH_TO_STORE_FILE + name + '.json') as f:
            json_file = json.load(f)
        return Response(json_file, status=200)

    def post(self, request):
        """
        Required that the client is authenticated,
        This method load a file from the json and save it on the disk
        :param request: the file in json Base64 format
        :return: the key to get to that file after.
        """
        serializer = FileToFilesystemSerializer(
            path=settings.PATH_TO_STORE_FILE, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.instance,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def put(self, request):
    #     """
    #     Required that the client is authenticated,
    #     This method load a file from the json and update it on the disk
    #     (NotImplemented)
    #     :param request: the key and the new file in json Base64 format
    #     :return: the key to get to that file after.
    #     """
    #     raise NotImplemented()


class RouterViewSet(viewsets.ViewSet):
    """
    Sample API to retreive, update, add and delete router details.

    Makes use of rest_framework.viewsets.ViewSet to expose APIs.
    """

    def get_queryset(self):
        queryset = RouterDetails.objects.filter(is_deleted=False)
        return queryset

    def list(self, request):
        """
        Required that the client is authenticated,
        This method lists all the router data and sends JSON response.
        This method responds to GET request.
        :param request: the request from the client to fetch all the details.
        :return: JSON response of the router data
        """
        queryset = self.get_queryset()
        serializer_class = RouterSerializer(queryset, many=True)
        return Response(serializer_class.data)

    def retrieve(self, request, pk=None):
        """
        Required that the client is authenticated,
        This method fetches the router data and sends JSON response.
        This method responds to GET request.
        :param request: the request from the client to fetch the details.
        :param pk: the record id to retrieve
        :return: JSON response of the router data
        """
        queryset = self.get_queryset()
        router = get_object_or_404(queryset, pk=pk)
        serializer_class = RouterSerializer(router)
        return Response(serializer_class.data)

    def create(self, request):
        """
        Required that the client is authenticated,
        This method adds new router data in database and sends JSON response.
        This method responds to POST requests
        :param request: the request from the client to add the details.
        :return: JSON response of the router data
        """
        data = request.data
        serializer_class = RouterSerializer(data=data)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """
        Required that the client is authenticated,
        This method updates router record and sends its status in response.
        This method responds to PUT request.
        :param request: the request from the client to update router data, contains router data.
        :param pk: the record id to update
        :return: HTTP status message on record update else sends error message.
        """
        data = request.data
        queryset = self.get_queryset()
        router = get_object_or_404(queryset, pk=pk)
        serializer_class = RouterSerializer(router, data=data)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(serializer_class.data)
        return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """
        Required that the client is authenticated,
        This method marks router record as deleted and sends its status in response.
        This method responsds to DELETE requests.
        :param request: the request object the client.
        :param pk: the record id to delete
        :return: HTTP status message on record delete.
        """
        queryset = self.get_queryset()
        router = get_object_or_404(queryset, pk=pk)
        router.is_deleted = True
        router.save()
        return Response(status=status.HTTP_204_NO_CONTENT)