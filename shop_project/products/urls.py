from django.urls import path

from .views import CategoryListView, ProductListView, CartItemCreateView, \
    CartItemUpdateView, CartItemDeleteView, CartSummaryView, ClearCartView

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('cart/add/', CartItemCreateView.as_view(), name='cart-add'),
    path('cart/update/<int:pk>/', CartItemUpdateView.as_view(),
         name='cart-update'),
    path('cart/delete/<int:pk>/', CartItemDeleteView.as_view(),
         name='cart-delete'),
    path('cart/summary/', CartSummaryView.as_view(), name='cart-summary'),
    path('cart/clear/', ClearCartView.as_view(), name='cart-clear'),
]
