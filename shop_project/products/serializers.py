from rest_framework import serializers

from .models import Category, SubCategory, Product, CartItem


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['name', 'slug', 'category', 'subcategory', 'price', 'images']

    def get_category(self, obj):
        """Возвращает название категории"""
        return obj.subcategory.parent_category.name

    def get_images(self, obj):
        """Возвращает URL изображений"""
        return {
            'small': obj.image_small.url,
            'medium': obj.image_medium.url,
            'large': obj.image_large.url,
        }


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['name', 'slug', 'image']


class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['name', 'slug', 'image', 'subcategories']


class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(
        source='product.name',
        read_only=True
    )
    price = serializers.DecimalField(
        source='product.price',
        max_digits=10,
        decimal_places=2,
        read_only=True
    )

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_name', 'price', 'quantity']

    def create(self, validated_data):
        """ Создание нового элемента корзины """
        user = self.context['request'].user
        product = validated_data.get('product')
        quantity = validated_data.get('quantity')
        cart_item, created = CartItem.objects.get_or_create(
            user=user,
            product=product
        )
        if not created:
            cart_item.quantity += quantity
        cart_item.save()
        return cart_item


class CartSummarySerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(
        source='product.name',
        read_only=True
    )
    price = serializers.DecimalField(
        source='product.price',
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['product_name', 'price', 'quantity', 'total_price']

    def get_total_price(self, obj):
        return obj.quantity * obj.product.price
