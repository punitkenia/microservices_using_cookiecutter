from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status

from .models import RouterDetails
from .serializers import  RouterSerializer

# Create your views here.
class RouterViewSet(viewsets.ViewSet):

    def get_queryset(self):
        queryset = RouterDetails.objects.filter(is_deleted=False)
        return queryset

    def list(self, request):
        queryset = self.get_queryset()
        serializer_class = RouterSerializer(queryset, many=True)
        return Response(serializer_class.data)

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()
        router = get_object_or_404(queryset, pk=pk)
        serializer_class = RouterSerializer(router)
        return Response(serializer_class.data)

    def create(self, request):
        data = request.data
        serializer_class = RouterSerializer(data=data)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        data = request.data
        queryset = self.get_queryset()
        router = get_object_or_404(queryset, pk=pk)
        serializer_class = RouterSerializer(router, data=data)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(serializer_class.data)
        return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        queryset = self.get_queryset()
        router = get_object_or_404(queryset, pk=pk)
        router.is_deleted = True
        router.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
