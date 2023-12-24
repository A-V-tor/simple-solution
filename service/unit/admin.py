from django.contrib import admin
from unit.models import Item, Order, Discount, Tax

# Register your models here.


class ItemAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description',
        'price',
    )


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'data_item',
        'is_paid',
        'user',
    )


class DiscountAdmin(admin.ModelAdmin):
    list_display = (
        'percent',
        'duration',
        'duration_in_month',
    )


class TaxAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'inclusive', 'percentage', 'country')


admin.site.register(Item, ItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Discount, DiscountAdmin)
admin.site.register(Tax, TaxAdmin)
