from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from products.models import Product
import uuid

class User(AbstractUser):
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    red_cards = models.IntegerField(default=0)
    yellow_cards = models.IntegerField(default=0)
    telegram_chat_id = models.CharField(max_length=100, blank=True, null=True)
    telegram_token = models.UUIDField(default=uuid.uuid4, null=True, blank=True)

    def __str__(self):
        return self.username

class PurchaseHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='purchase_history', on_delete=models.CASCADE)
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.order.order_number}'
