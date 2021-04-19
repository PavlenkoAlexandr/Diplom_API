from rest_framework import serializers

from reviews.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'id', 'author_id', 'product_id', 'text', 'rating', 'created_date', 'updated_date'
    rating = serializers.IntegerField(min_value=1, max_value=5)

    def validate(self, attrs):
        if attrs.get('author_id'):
            for row in list(Review.objects.all().filter(author_id=attrs.get('author_id').id).select_related('product_id')):
                if attrs.get('product_id').id == row.product_id_id:
                    raise serializers.ValidationError('1 пользователь не может оставлять более 1го отзыва')
        return attrs
