import requests
from django.conf import settings
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from django.utils.decorators import method_decorator

from brew_warehouse import models, serializers
import json

BEARER_SECURITY = [{'Bearer': []}]


@method_decorator(name='list', decorator=swagger_auto_schema(security=BEARER_SECURITY))
@method_decorator(name='create', decorator=swagger_auto_schema(security=BEARER_SECURITY))
class WarehouseItemViewSet(viewsets.ModelViewSet):
    queryset = models.WarehouseItem.objects.all()
    serializer_class = serializers.WarehouseItemSerializer
    http_method_names = ['post', 'get', 'delete']

    def _check_auth(self):
        """Check JWT auth token validity"""
        try:
            auth_token = self.request.META.get('HTTP_AUTHORIZATION', '')
        except IndexError:
            return Response(
                "Authorization header does not contain valid JWT token",
                status=status.HTTP_403_FORBIDDEN
            )
        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
        response = requests.post(
            settings.AUTH_SERVICE_VERIFY_JWT_URL, data=json.dumps({'token': auth_token}))
        if not response.status_code == status.HTTP_200_OK:
            return Response("Authorization header does not contain valid JWT token", status=status.HTTP_403_FORBIDDEN)

    def list(self, reqeust):
        """List all warehouse items.

        in parameter: Authorization Header {'token': 'valid JWT auth token'}
        """
        self._check_auth()
        items = self.get_queryset()
        serializer = self.serializer_class(items, many=True)
        return Response(serializer.data)

    def create(self, reqeust):
        """Create a warehouse item.

        in parameter: Authorization Header {'token': 'valid JWT auth token'}
        """
        self._check_auth()
        warehouse_item = self.serializer_class(data=self.request.data)
        warehouse_item.is_valid(raise_exception=True)
        advice_obj = warehouse_item.save()
        return Response('Created warehouse item', status=status.HTTP_201_CREATED)
