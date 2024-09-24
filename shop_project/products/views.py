from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Category, Product, CartItem, SubCategory
from .serializers import CategorySerializer, ProductSerializer, \
    CartItemSerializer, CartSummarySerializer


class ProductPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all().order_by('name')
    serializer_class = ProductSerializer
    pagination_class = ProductPagination
    permission_classes = [AllowAny]


class CategoryPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    pagination_class = CategoryPagination
    permission_classes = [AllowAny]


class CartItemCreateView(generics.CreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """ Создание корзины для пользователя """
        serializer.save(user=self.request.user)


class CartItemUpdateView(generics.UpdateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """ Получение корзины для пользователя """
        if getattr(self, 'swagger_fake_view', False):
            return CartItem.objects.none()
        return CartItem.objects.filter(user=self.request.user)


class CartItemDeleteView(generics.DestroyAPIView):
    queryset = CartItem.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """ Получение корзины для пользователя """
        if getattr(self, 'swagger_fake_view', False):
            return CartItem.objects.none()
        return CartItem.objects.filter(user=self.request.user)


class CartSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """ Сводная информация о корзине """
        cart_items = CartItem.objects.filter(user=request.user)
        serializer = CartSummarySerializer(cart_items, many=True)

        total_quantity = sum(item['quantity'] for item in serializer.data)
        total_price = sum(item['total_price'] for item in serializer.data)

        return Response({
            'cart_items': serializer.data,
            'total_quantity': total_quantity,
            'total_price': total_price
        })


class ClearCartView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        """ Очистка корзины """
        CartItem.objects.filter(user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def category_list(request):
    """ Список категорий """
    categories = Category.objects.prefetch_related('subcategories').all()
    return render(request, 'products/index.html', {'categories': categories})


def product_list(request, subcategory_slug):
    """ Список продуктов в категории """
    subcategory = get_object_or_404(SubCategory, slug=subcategory_slug)
    products = subcategory.products.all()
    return render(
        request, 'products/product_list.html',
        {'products': products, 'subcategory': subcategory}
    )


def cart_view(request):
    """ Корзина """
    cart_items = CartItem.objects.filter(user=request.user).select_related(
        'product')
    total_price = sum(item.quantity * item.product.price for item in cart_items)
    return render(
        request, 'products/cart.html',
        {'cart_items': cart_items, 'total_price': total_price}
    )
