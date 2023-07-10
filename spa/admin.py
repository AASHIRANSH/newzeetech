from django.contrib import admin
from .sales.models import Client, Sale, Item, Referrer
from .accounts.models import Receipt #,Payment


@admin.register(Receipt)
class ReceiptView(admin.ModelAdmin):
    list_display = ('sale','amount','date')


@admin.register(Client)
class ClientView(admin.ModelAdmin):
    list_display = ('id','name','company')


@admin.register(Referrer)
class ReferrerView(admin.ModelAdmin):
    list_display = ('name','company')


@admin.register(Sale)
class SaleView(admin.ModelAdmin):
    list_display = ('order_id','company','item_1')


@admin.register(Item)
class ItemView(admin.ModelAdmin):
    list_display = ('id','name','rate')


# admin.site.register(Sale, SaleView) #if you want to use this statement @admin.register above the SaleView must be disabled