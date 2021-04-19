from django.contrib import admin

from products.models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = 'name', 'description', 'price', 'created_date', 'updated_date'


admin.site.register(Product, ProductAdmin)
