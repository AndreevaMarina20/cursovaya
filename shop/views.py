from decimal import Decimal
from django.db import transaction
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from .models import (
    User,
    Category,
    Product,
    Cart,
    CartItem,
    Order,
    OrderItem,
)

from .serializers import (
    CategorySerializer,
    ProductSerializer,
    RegisterSerializer,
    CartSerializer,
    AddCartItemSerializer,
    UpdateCartItemSerializer,
    OrderSerializer,
    OrderItemSerializer,
    CreateOrderSerializer,
)


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Product.objects.filter(is_available=True)

        category_id = self.request.query_params.get('category')

        if category_id:
            queryset = queryset.filter(category_id=category_id)

        return queryset


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.filter(is_available=True)
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


# Получение корзины и добавление товаров
class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart, created = Cart.objects.get_or_create(
            user=request.user
        )

        serializer = CartSerializer(
            cart,
            context={'request': request}
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = AddCartItemSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)

        product = serializer.validated_data['product']
        quantity = serializer.validated_data['quantity']

        cart, created = Cart.objects.get_or_create(
            user=request.user
        )

        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )

        if not created:
            item.quantity += quantity
            item.save()

        return Response(
            CartSerializer(
                cart,
                context={'request': request}
            ).data,
            status=status.HTTP_200_OK
        )


# Изменение количества и удаление товара
class CartItemView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        cart = get_object_or_404(
            Cart,
            user=request.user
        )
        item = get_object_or_404(
            CartItem,
            pk=pk,
            cart=cart
        )

        serializer = UpdateCartItemSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)

        item.quantity = serializer.validated_data['quantity']
        item.save()

        return Response(
            CartSerializer(
                cart,
                context={'request': request}
            ).data
        )

    def delete(self, request, pk):
        cart = get_object_or_404(
            Cart,
            user=request.user
        )
        item = get_object_or_404(
            CartItem,
            pk=pk,
            cart=cart
        )

        item.delete()

        return Response(
            CartSerializer(
                cart,
                context={'request': request}
            ).data
        )


# Оформление заказа
class OrderCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        serializer = CreateOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cart = Cart.objects.filter(
            user=request.user
        ).first()

        if not cart or not cart.items.exists():
            return Response(
                {'error': 'Корзина пуста'},
                status=status.HTTP_400_BAD_REQUEST
            )

        cart_items = list(
            cart.items.select_related('product')
        )

        total = sum(
            (
                item.product.price * item.quantity
                for item in cart_items
            ),
            Decimal('0.00')
        )

        order = Order.objects.create(
            user=request.user,
            customer_name=serializer.validated_data['customer_name'],
            phone=serializer.validated_data['phone'],
            address=serializer.validated_data['address'],
            total=total,
            status='new'
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                product_name=item.product.name,
                price=item.product.price,
                quantity=item.quantity
            )

        cart.items.all().delete()

        return Response(
            OrderSerializer(
                order,
                context={'request': request}
            ).data,
            status=status.HTTP_201_CREATED
        )


# История заказов пользователя
class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(
            user=self.request.user
        ).order_by('-created_at')


# Просмотр отдельного заказа и его статуса
class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(
            user=self.request.user
        )
