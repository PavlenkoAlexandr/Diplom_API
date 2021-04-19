from django_filters import rest_framework as filters


class ReviewsFilterSet(filters.FilterSet):

    author_id = filters.CharFilter(field_name='author_id', lookup_expr='exact')
    product_id = filters.NumberFilter(field_name='product_id', lookup_expr='exact')
    created_date = filters.DateFilter(field_name='created_date', lookup_expr='icontains')
