from django.contrib import admin

from .models import News, Product, Cart, CartItem

class CartItemInline(admin.TabularInline):
    model = Cart.products.through
    extra = 1

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    pass

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemInline]
    pass

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    pass
