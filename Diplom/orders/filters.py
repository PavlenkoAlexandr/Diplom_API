from django_filters import rest_framework as filters

from orders.models import Order


class OrdersFilterSet(filters.FilterSet):

    queryset = Order.objects.prefetch_related('order_positions').all()

    status = filters.CharFilter(field_name='status', lookup_expr='exact')
    created_date = filters.DateFilter(field_name='created_date', lookup_expr='icontains')
    updated_date = filters.DateFilter(field_name='updated_date', lookup_expr='icontains')
    product = filters.CharFilter(field_name='order_positions__product__name', lookup_expr='icontains')
    amount = filters.NumberFilter(field_name='amount', lookup_expr='exact')
    amount_from = filters.NumberFilter(field_name="amount", lookup_expr="gte")
    amount_to = filters.NumberFilter(field_name="amount", lookup_expr="lte")

