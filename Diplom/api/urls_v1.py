from rest_framework.routers import DefaultRouter

from orders.views import OrderViewSet
from product_collections.views import CollectionViewSet
from products.views import ProductViewSet
from reviews.views import ReviewViewSet

router = DefaultRouter()
router.register('orders', OrderViewSet, basename='orders')
router.register('products', ProductViewSet, basename='products')
router.register('product-reviews', ReviewViewSet, basename='product-reviews')
router.register('product-collections', CollectionViewSet, basename='product-collections')

urlpatterns = router.urls
