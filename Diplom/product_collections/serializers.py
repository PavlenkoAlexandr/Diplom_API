from rest_framework import serializers
from product_collections.models import ProductCollectionPosition, Collection


class ProductCollectionPositionSerializer(serializers.ModelSerializer):

    product_id = serializers.IntegerField()

    class Meta:
        model = ProductCollectionPosition
        fields = 'product_id', 'quantity'

    quantity = serializers.IntegerField(min_value=1, default=1)


class CollectionSerializer(serializers.ModelSerializer):

    positions = ProductCollectionPositionSerializer(many=True, source='collection_positions')

    class Meta:
        model = Collection
        fields = 'id', 'title', 'positions', 'text', 'created_date', 'updated_date'

    def create(self, validated_data):
        positions = validated_data.pop('collection_positions')
        collection = super().create(validated_data)
        if positions:
            to_save = list()
            for position in positions:
                to_save.append(ProductCollectionPosition(
                    product_id=position['product_id'],
                    collection_id=collection.id,
                    quantity=position['quantity']
                ))
            ProductCollectionPosition.objects.bulk_create(to_save)
        return collection

    def validate_positions(self, value):
        if not value:
            raise serializers.ValidationError('Не указанны коллекции')
        products_ids = [item['product_id'] for item in value]
        if len(products_ids) != len(set(products_ids)):
            raise serializers.ValidationError('Дублируются позиции в коллекции')
        return value
