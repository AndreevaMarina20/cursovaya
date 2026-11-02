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
    path('categories/', CategoryListView.as_view()),        #категории
    path('products/', ProductListView.as_view()),       #меню
    path('products/<int:pk>/', ProductDetailView.as_view()),        #информация одного блюда из меню

    path('auth/register/', RegisterView.as_view()),     #регистрация нового пользователя
    path('auth/login/', TokenObtainPairView.as_view()),     #вход и выдача jwt-токена для пользования корзиной.
    path('auth/token/refresh/', TokenRefreshView.as_view()),        #продление доступа в аккаунте

    path('cart/', CartView.as_view()),      #get-корзина текущего пользователя. post-добавляет товар в корзину
    path('cart/items/<int:pk>/', CartItemView.as_view()),       #patch-изменяет количество конкретного товара в корзине. delete-удаляет конкрентную позицию из корзины

    path('orders/', OrderListView.as_view()),       #история заказов текущего пользователя
    path('orders/create/', OrderCreateView.as_view()),      #создает заказ на основе корзины
    path('orders/<int:pk>/', OrderDetailView.as_view()),        #показывает подробную информацию о конкретном заказе
]