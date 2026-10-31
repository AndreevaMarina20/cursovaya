
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (
    User,
    Category,
    Product,
    Cart,
    CartItem,
    Order,
    OrderItem,
)


# Пользователи
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (
            'Дополнительная информация',
            {'fields': ('phone', 'address')}
        ),
    )


# Категории
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


# Товары
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'category',
        'price',
        'is_available',
    )
    list_filter = ('category', 'is_available')
    search_fields = ('name',)


# Позиции корзины
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


# Корзины
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'session_key',
        'created_at',
    )
    inlines = [CartItemInline]


# Позиции заказа
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = (
        'product',
        'product_name',
        'price',
        'quantity',
    )


# Заказы
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'customer_name',
        'status',
        'total',
        'created_at',
    )
    list_filter = ('status', 'created_at')
    readonly_fields = ('total', 'created_at')
    inlines = [OrderItemInline]
