import requests
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from brew_warehouse import models, serializers


class WarehouseItemViewSet(viewsets.ModelViewSet):
    queryset = models.WarehouseItem.objects.all()
    serializer_class = serializers.WarehouseItemSerializer
    http_method_names = ['post', 'get', 'delete']

    def list(self, reqeust):
        auth_token = self.request.META.get('HTTP_AUTHORIZATION', '').split()[1]
        requests.post(settings.AUTH_SERVICE_VERIFY_JWT_URL, data={'token': auth_token})
        items = self.get_queryset()
        serializer = self.serializer_class(items, many=True)
        return Response(serializer.data)
