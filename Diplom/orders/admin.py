from django.contrib import admin

from orders.models import Order, ProductOrderPosition


class ProductOrderPositionInline(admin.TabularInline):
    model = ProductOrderPosition


class OrderAdmin(admin.ModelAdmin):

    list_display = ('id', 'user_id', 'amount', 'status', 'created_date', 'updated_date')
    inlines = (ProductOrderPositionInline,)


admin.site.register(Order, OrderAdmin)
