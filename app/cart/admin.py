from django.contrib import admin

from app.cart.models import Basket, Line


@admin.register(Line)
class LineAdmin(admin.ModelAdmin):
    pass


class LineInline(admin.TabularInline):
    model = Line
    readonly_fields = ('product', 'price', 'currency')


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'num_lines',
                    'created', 'currency', 'total')
    readonly_fields = ('user', 'date_submitted')
    inlines = [LineInline]
