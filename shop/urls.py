from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (
    CategoryListView,
    ProductListView,
    ProductDetailView,
    RegisterView,
    CartView,
    CartItemView,
    OrderCreateView,
    OrderListView,
    OrderDetailView,
)

urlpatterns = [
    path('categories/', CategoryListView.as_view()),
    path('products/', ProductListView.as_view()),
    path('products/<int:pk>/', ProductDetailView.as_view()),

    path('auth/register/', RegisterView.as_view()),
    path('auth/login/', TokenObtainPairView.as_view()),
    path('auth/token/refresh/', TokenRefreshView.as_view()),

    path('cart/', CartView.as_view()),
    path('cart/items/<int:pk>/', CartItemView.as_view()),

    path('orders/', OrderListView.as_view()),
    path('orders/create/', OrderCreateView.as_view()),
    path('orders/<int:pk>/', OrderDetailView.as_view()),
]