from django.contrib.auth.models import AbstractUser
from django.db import models
from products.models import Product  # Импорт модели Product из приложения products

class User(AbstractUser):
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    red_cards = models.IntegerField(default=0)
    yellow_cards = models.IntegerField(default=0)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',  # Add related_name to avoid clashes
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',  # Add related_name to avoid clashes
        blank=True
    )

    def __str__(self):
        return self.username

class PurchaseHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchase_history')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Ссылка на модель Product из приложения products
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.product.name} - {self.date}'
