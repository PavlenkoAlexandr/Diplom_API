from django.contrib import admin

from reviews.models import Review


class ReviewAdmin(admin.ModelAdmin):
    list_display = 'author_id', 'product_id', 'text', 'rating', 'created_date', 'updated_date'


admin.site.register(Review, ReviewAdmin)
