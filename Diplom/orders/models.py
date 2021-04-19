from django.db import models
from django.utils import timezone
from products.models import Product
from django.contrib.auth.models import User


class Order(models.Model):

    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    positions = models.ManyToManyField(Product, through='ProductOrderPosition')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, editable=False)
    status = models.CharField(max_length=15, default='NEW')
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Заказ №{self.id}'

    def save(self, *args, **kwargs):
        purchase = self.order_positions.values_list('product_id', 'quantity')
        self.amount = sum([Product.objects.get(id=i[0]).price * i[1] for i in purchase])
        super().save(*args, **kwargs)

class ProductOrderPosition(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, related_name='order_positions', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        order = Order.objects.get(id=self.order_id)
        order.save()
