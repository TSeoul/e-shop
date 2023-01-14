from django.contrib import admin

# Register your models here.
from .models import Order, CartItem, Order, Cart

class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at')

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name','address','postal_code','city','created_at','updated_at','ordered','total_price')

admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Order, OrderAdmin)


