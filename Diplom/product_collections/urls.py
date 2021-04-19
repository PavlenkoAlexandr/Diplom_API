from product_collections.views import CollectionViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('collections', CollectionViewSet)

urlpatterns = router.urls
