from django.contrib import admin

from product_collections.models import Collection, ProductCollectionPosition


class ProductCollectionPositionInline(admin.TabularInline):
    model = ProductCollectionPosition


class CollectionAdmin(admin.ModelAdmin):
    list_display = 'title', 'text', 'created_date', 'updated_date'
    inlines = (ProductCollectionPositionInline,)


admin.site.register(Collection, CollectionAdmin)
