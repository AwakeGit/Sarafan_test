from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.contrib.auth.models import User

from .models import Category, SubCategory, Product, CartItem

# Сначала отменяем регистрацию модели User с использованием стандартного UserAdmin
admin.site.unregister(User)


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0  # Не добавлять пустые строки для новых элементов
    readonly_fields = ('product', 'quantity', 'total_price')

    def total_price(self, obj):
        return obj.quantity * obj.product.price

    total_price.short_description = 'Total Price'


# Теперь регистрируем модель User с кастомной админкой
@admin.register(User)
class UserCartAdmin(DefaultUserAdmin):
    list_display = ('username', 'total_items', 'total_cart_price')
    inlines = [CartItemInline]  # Инлайн для отображения корзин пользователя

    def total_items(self, obj):
        # Считаем количество товаров в корзине пользователя
        return CartItem.objects.filter(user=obj).count()

    def total_cart_price(self, obj):
        # Считаем общую стоимость корзины для данного пользователя
        cart_items = CartItem.objects.filter(user=obj)
        return sum(item.quantity * item.product.price for item in cart_items)

    total_items.short_description = 'Total Items'
    total_cart_price.short_description = 'Total Cart Price'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'parent_category')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'price', 'subcategory', 'category')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'slug']
    list_filter = ['subcategory']


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'total_price')
    list_filter = ('user', 'product')
    search_fields = ('user__username', 'product__name')

    def total_price(self, obj):
        return obj.quantity * obj.product.price

    total_price.short_description = 'Total Price'
