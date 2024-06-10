from rest_framework import serializers
from .models import User, PurchaseHistory
from products.models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class PurchaseHistorySerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = PurchaseHistory
        fields = ['product', 'date']

class UserProfileSerializer(serializers.ModelSerializer):
    purchase_history = PurchaseHistorySerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['username', 'balance', 'red_cards', 'yellow_cards', 'purchase_history']


class UserStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'balance', 'red_cards', 'yellow_cards']