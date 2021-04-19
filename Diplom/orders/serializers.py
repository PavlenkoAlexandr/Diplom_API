from rest_framework import serializers

from orders.models import Order, ProductOrderPosition


class ProductOrderPositionSerializer(serializers.ModelSerializer):

    product_id = serializers.IntegerField()

    class Meta:
        model = ProductOrderPosition
        fields = 'product_id', 'quantity'

    quantity = serializers.IntegerField(min_value=1, default=1)


class OrderSerializer(serializers.ModelSerializer):

    positions = ProductOrderPositionSerializer(many=True, source='order_positions')

    class Meta:
        model = Order
        fields = 'id', 'user_id', 'positions', 'status', 'created_date', 'updated_date', 'amount'

    def create(self, validated_data):
        positions = validated_data.pop('order_positions')
        order = super().create(validated_data)
        if positions:
            to_save = list()
            for position in positions:
                to_save.append(ProductOrderPosition(
                    product_id=position['product_id'],
                    order_id=order.id,
                    quantity=position['quantity']
                ))
            ProductOrderPosition.objects.bulk_create(to_save)
            order.save()
        return order

    def validate_positions(self, value):
        if not value:
            raise serializers.ValidationError('Не указанны позиции заказа')
        products_ids = [item['product_id'] for item in value]
        if len(products_ids) != len(set(products_ids)):
            raise serializers.ValidationError('Дублируются позиции в заказе')
        return value

    def validate_status(self, value):
        statuses = ['DONE', 'IN_PROGRESS', 'NEW']
        if value not in statuses:
            raise serializers.ValidationError('Неверный статус заказа')
        return value
