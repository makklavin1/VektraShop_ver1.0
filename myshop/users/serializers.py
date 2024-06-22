from rest_framework import serializers
from .models import User, PurchaseHistory
from products.models import Product
from orders.models import Order, OrderItem

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock', 'image']

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['order_number', 'status', 'created_at', 'updated_at', 'items']

class PurchaseHistorySerializer(serializers.ModelSerializer):
    order_number = serializers.CharField(source='order.order_number')
    items = OrderItemSerializer(source='order.items', many=True)
    created_at = serializers.DateTimeField(source='order.created_at')
    status = serializers.CharField(source='order.status')

    class Meta:
        model = PurchaseHistory
        fields = ['order_number', 'created_at', 'status', 'items']

class UserProfileSerializer(serializers.ModelSerializer):
    purchase_history = PurchaseHistorySerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['username', 'balance', 'red_cards', 'yellow_cards', 'purchase_history', 'telegram_chat_id', 'telegram_token']

class UserStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'balance', 'red_cards', 'yellow_cards']
