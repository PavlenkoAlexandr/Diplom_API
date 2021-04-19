from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet
from product_collections.models import Collection
from product_collections.serializers import CollectionSerializer


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.prefetch_related('collection_positions').all()
    serializer_class = CollectionSerializer
    permission_classes = [IsAdminUser]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return []
