from django.db import models
from django.conf import settings
from products.models import Product
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
import uuid
import logging

logger = logging.getLogger(__name__)


def send_telegram(chat_id, message, token=settings.TELEGRAM_BOT_TOKEN):
    import requests
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {'chat_id': chat_id, 'text': message}
    response = requests.post(url, data=data)
    response.raise_for_status()  # Это выбросит исключение, если запрос завершится неудачей
    return response.json()


class Order(models.Model):
    STATUS_CHOICES = [
        ('created', 'Created'),
        ('in_progress', 'In Progress'),
        ('awaiting_pickup', 'Awaiting Pickup'),
        ('completed', 'Completed'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Order {self.order_number} - {self.user.username}'

    def change_status(self, new_status):
        self.status = new_status
        self.save()
        logger.info(f"Статус заказа {self.order_number} изменен на {new_status}.")
        status_messages = {
            'in_progress': "Статус заказа изменен: Сборка",
            'awaiting_pickup': "Статус заказа изменен: Ожидает получения",
            'completed': "Заказ успешно получен"
        }
        message = status_messages.get(new_status,
                                      f"Статус заказа {self.order_number} изменен на {self.get_status_display()}.")
        try:
            send_telegram(self.user.telegram_chat_id, message)
            logger.info(f"Сообщение о статусе отправлено пользователю {self.user.username}: {message}")
        except Exception as e:
            logger.error(f"Ошибка при отправке сообщения пользователю: {e}")


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.product.name} ({self.quantity})'


@receiver(pre_save, sender=Order)
def check_order_status_change(sender, instance, **kwargs):
    if not instance.pk:
        # Новый заказ, изменений статуса нет
        return

    try:
        original_order = Order.objects.get(pk=instance.pk)
    except Order.DoesNotExist:
        return

    if original_order.status != instance.status:
        logger.info(f"Статус заказа {instance.order_number} изменен с {original_order.status} на {instance.status}.")
        status_messages = {
            'in_progress': "Статус заказа изменен: Сборка",
            'awaiting_pickup': "Статус заказа изменен: Ожидает получения",
            'completed': "Заказ успешно получен"
        }
        message = status_messages.get(instance.status,
                                      f"Статус заказа {instance.order_number} изменен на {instance.get_status_display()}.")
        try:
            send_telegram(instance.user.telegram_chat_id, message)
            logger.info(f"Сообщение о статусе отправлено пользователю {instance.user.username}: {message}")
        except Exception as e:
            logger.error(f"Ошибка при отправке сообщения пользователю: {e}")


@receiver(post_save, sender=Order)
def send_order_notifications(sender, instance, created, **kwargs):
    logger.info(f"send_order_notifications вызван для заказа {instance.order_number}")

    if created:
        logger.info("Создание нового заказа.")
        message = f"Спасибо, ваш заказ {instance.order_number} успешно создан."
        try:
            send_telegram(instance.user.telegram_chat_id, message)
            logger.info(
                f"Сообщение отправлено пользователю {instance.user.username} о создании заказа {instance.order_number}")
        except Exception as e:
            logger.error(f"Ошибка при отправке сообщения пользователю: {e}")

        admin_message = f"Новый заказ {instance.order_number} от {instance.user.username}."
        admin_chat_id = settings.TELEGRAM_ADMIN_CHAT_ID
        try:
            send_telegram(admin_chat_id, admin_message)
            logger.info(f"Сообщение отправлено администратору о создании заказа {instance.order_number}")
        except Exception as e:
            logger.error(f"Ошибка при отправке сообщения администратору: {e}")
    else:
        logger.info("Обновление заказа.")
        try:
            original_order = Order.objects.get(pk=instance.pk)
            original_status = original_order.status
            logger.info(f"Original status: {original_status}, New status: {instance.status}")
        except Order.DoesNotExist:
            original_status = None

        if original_status and original_status != instance.status:
            logger.info(f"Статус заказа {instance.order_number} изменен с {original_status} на {instance.status}.")
            status_messages = {
                'in_progress': "Статус заказа изменен: Сборка",
                'awaiting_pickup': "Статус заказа изменен: Ожидает получения",
                'completed': "Заказ успешно получен"
            }
            message = status_messages.get(instance.status,
                                          f"Статус заказа {instance.order_number} изменен на {instance.get_status_display()}.")
            try:
                send_telegram(instance.user.telegram_chat_id, message)
                logger.info(f"Сообщение о статусе отправлено пользователю {instance.user.username}: {message}")
            except Exception as e:
                logger.error(f"Ошибка при отправке сообщения пользователю: {e}")
        else:
            logger.info(f"Статус заказа {instance.order_number} не изменился или оригинальный статус не найден.")
