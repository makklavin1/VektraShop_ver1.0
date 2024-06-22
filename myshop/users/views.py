from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.conf import settings
from .models import User, PurchaseHistory
from orders.models import Order, OrderItem
from products.models import Product
from .serializers import UserProfileSerializer, UserStatsSerializer, PurchaseHistorySerializer, OrderSerializer
import logging
import uuid

logger = logging.getLogger(__name__)

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        logger.info("Login attempt for user: %s", request.data.get('username'))
        response = super(CustomAuthToken, self).post(request, *args, **kwargs)
        if 'token' in response.data:
            token = Token.objects.get(key=response.data['token'])
            logger.info("Login successful for user: %s", token.user.username)
            return Response({'token': token.key, 'user_id': token.user_id, 'email': token.user.email})
        else:
            logger.error("Login failed for user: %s", request.data.get('username'))
            return Response(response.data, status=response.status_code)

@login_required
def profile(request):
    logger.info("Profile view called")
    return render(request, 'users/profile.html', {'user': request.user})

class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class UserStatsView(generics.ListAPIView):
    queryset = User.objects.filter(is_superuser=False)
    serializer_class = UserStatsSerializer
    permission_classes = [IsAuthenticated]

class CheckoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        cart_items = request.data.get('cart_items', [])

        logger.info("Received cart items: %s", cart_items)

        total_cost = 0
        for item in cart_items:
            try:
                product = Product.objects.get(id=item['id'])
                if product.stock < item['quantity']:
                    return Response({'error': f'Not enough stock for product {product.name}'}, status=status.HTTP_400_BAD_REQUEST)
                total_cost += product.price * item['quantity']
            except Product.DoesNotExist:
                return Response({'error': f'Product with id {item["id"]} does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        if user.balance < total_cost:
            return Response({'error': 'Insufficient balance'}, status=status.HTTP_400_BAD_REQUEST)

        # Deduct the amount from user's balance
        user.balance -= total_cost
        user.save()

        # Create order and order items
        order = Order.objects.create(
            user=user,
            order_number=str(uuid.uuid4()),
            status='created'
        )
        for item in cart_items:
            product = Product.objects.get(id=item['id'])
            OrderItem.objects.create(order=order, product=product, quantity=item['quantity'])
            product.stock -= item['quantity']
            product.save()

        return Response({'message': 'Order created successfully'}, status=status.HTTP_200_OK)

class UserOrdersView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(user=user).exclude(status='completed')

class PurchaseHistoryView(generics.ListAPIView):
    serializer_class = PurchaseHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return PurchaseHistory.objects.filter(user=user)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def link_telegram(request):
    user = request.user
    telegram_token = user.telegram_token  # Используем токен пользователя
    if telegram_token:
        telegram_url = f"https://t.me/vektrashop_bot?start={telegram_token}"
        return Response({"telegram_url": telegram_url})
    return Response({"error": "Telegram token is missing."}, status=400)
