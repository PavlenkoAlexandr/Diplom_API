from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status
from rest_framework.permissions import IsAuthenticated, BasePermissionMetaclass, IsAdminUser
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.viewsets import ModelViewSet

from orders.filters import OrdersFilterSet
from orders.models import Order
from orders.serializers import OrderSerializer
from orders.permissions import IsOwner


class OrderViewSet(ModelViewSet):

    queryset = Order.objects.prefetch_related('order_positions').all()
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrdersFilterSet


    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        elif self.action in ['create']:
            return [IsAuthenticated()]
        elif self.action in ['retrieve']:
            return [IsOwner()]
        elif self.action in ['list']:
            return [IsAuthenticated()]

    def list(self, request, *args, **kwargs):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return super().list(request, *args, **kwargs)
        queryset = self.filter_queryset(self.get_queryset()).filter(user_id=request.user.id)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        request.data['user_id'] = request.user.id
        return super(OrderViewSet, self).create(request)
