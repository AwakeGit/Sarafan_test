from decimal import Decimal

import pytest
from django.urls import reverse
from products.models import User, Category, SubCategory, Product, CartItem
from rest_framework import status
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestProductAPI:
    client = APIClient()

    @pytest.fixture(autouse=True)
    def set_up(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.client.force_authenticate(user=self.user)

        self.category = Category.objects.create(
            name='Electronics',
            slug='electronics'
        )
        self.subcategory = SubCategory.objects.create(
            name='Mobile Phones',
            slug='mobile-phones',
            parent_category=self.category
        )

        # Создание продуктов
        self.product = Product.objects.create(
            name='Smartphone',
            slug='smartphone',
            price=699.99,
            subcategory=self.subcategory,
            image_small='path/to/small/image.jpg',
            image_medium='path/to/medium/image.jpg',
            image_large='path/to/large/image.jpg'
        )

    def test_category_list(self):
        url = reverse('category-list')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) > 0

    def test_product_list(self):
        url = reverse('product-list')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) > 0

    def test_add_cart_item(self):
        url = reverse('cart-add')
        data = {'product': self.product.id, 'quantity': 1}
        response = self.client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert CartItem.objects.count() == 1

    def test_update_cart_item(self):
        cart_item = CartItem.objects.create(
            user=self.user,
            product=self.product,
            quantity=1
        )
        url = reverse('cart-update', kwargs={'pk': cart_item.id})
        data = {'quantity': 2}
        response = self.client.patch(
            url, data,
            format='json'
        )

        assert response.status_code == status.HTTP_200_OK
        cart_item.refresh_from_db()
        assert cart_item.quantity == 2

    def test_delete_cart_item(self):
        cart_item = CartItem.objects.create(
            user=self.user,
            product=self.product,
            quantity=1
        )
        url = reverse('cart-delete', kwargs={'pk': cart_item.id})
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert CartItem.objects.count() == 0

    def test_cart_summary(self):
        cart_item = CartItem.objects.create(
            user=self.user,
            product=self.product,
            quantity=2
        )
        url = reverse('cart-summary')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['total_quantity'] == 2
        expected_total_price = Decimal(cart_item.quantity) * Decimal(
            cart_item.product.price)
        expected_total_price = expected_total_price.quantize(
            Decimal('0.01'))
        response_total_price = Decimal(response.data['total_price']).quantize(
            Decimal('0.01'))

        assert response_total_price == expected_total_price
