from django.contrib import admin

from app.catalogue.models import Product, ProductClass


@admin.register(ProductClass)
class ProductClassAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    list_display = ('title', 'product_class', 'created', 'currency', 'price')
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ['title', ]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('product_class')
