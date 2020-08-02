from django.contrib import admin
from app.order.models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'created', 'currency', 'total')
    readonly_fields = ('user', 'created')
    raw_id_fields = ('user',)
