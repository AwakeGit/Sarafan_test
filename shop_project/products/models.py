from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(
        max_length=255,
        null=False,

        blank=False
    )

    slug = models.SlugField(
        unique=True,
        null=False,
        blank=False
    )
    image = models.ImageField(
        upload_to='category_images/',
        null=False,
        blank=False
    )

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(
        max_length=255,
        null=False,
        blank=False
    )
    slug = models.SlugField(
        unique=True,
        null=False,
        blank=False
    )
    image = models.ImageField(
        upload_to='subcategory_images/',
        null=False,
        blank=False
    )
    parent_category = models.ForeignKey(
        Category,
        related_name='subcategories',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        max_length=255,
        null=False,
        blank=False
    )
    slug = models.SlugField(
        unique=True,
        null=False,
        blank=False
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=False,
        blank=False
    )
    image_small = models.ImageField(
        upload_to='product_images/small/',
        null=False,
        blank=False
    )
    image_medium = models.ImageField(
        upload_to='product_images/medium/',
        null=False,
        blank=False
    )
    image_large = models.ImageField(
        upload_to='product_images/large/',
        null=False,
        blank=False
    )
    subcategory = models.ForeignKey(
        SubCategory,
        related_name='products',
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )

    @property
    def category(self):
        return self.subcategory.parent_category

    def __str__(self):
        return self.name


class CartItem(models.Model):
    user = models.ForeignKey(
        User,
        related_name='cart_items',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        related_name='cart_items',
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.product.name} (x{self.quantity}) - {self.user.username}'

    class Meta:
        unique_together = ('user', 'product')
