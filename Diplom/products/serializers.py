from rest_framework import serializers

from products.models import Product


class ProductSerializer(serializers.ModelSerializer):

    price = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0.01,)

    class Meta:
        model = Product
        fields = 'id', 'name', 'description', 'price', 'created_date', 'updated_date'
