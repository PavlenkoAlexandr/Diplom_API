from django.db import models
from django.utils import timezone

from products.models import Product


class Collection(models.Model):

    title = models.TextField()
    text = models.TextField()
    positions = models.ManyToManyField(Product, through='ProductCollectionPosition')
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)


class ProductCollectionPosition(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    collection = models.ForeignKey(Collection, related_name='collection_positions', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
