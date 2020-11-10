from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .tasks import send_email_task

import pprint
import logging

logger = logging.getLogger('django')

class BulkEmailApi(APIView):
    """
    Bulk Email Api
    """

    def post(self, request):
        # pprint.pprint (request.data)
        # logger.info('{"Incoming Data": {0}}'.format(request.data))
        logger.info(request.data)

        try:
            email = send_email_task.delay(request.data['body'],
            request.data['subject'], 
            request.data['from'], 
            request.data['to'])

            return Response({'Message': 'Email sent successfully'}, 
            status=status.HTTP_201_CREATED)

        except Exception as ex:
            logger.exception("BulkEmailApi Post raised an exception: " + str(ex))
            return Response({'Message': 'Error'}, status=status.HTTP_400_BAD_REQUEST)