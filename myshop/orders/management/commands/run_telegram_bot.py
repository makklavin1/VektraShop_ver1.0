# orders/management/commands/run_telegram_bot.py

from django.core.management.base import BaseCommand
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext
import os
from django.conf import settings
import django
import logging
from asgiref.sync import sync_to_async

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myshop.settings')
django.setup()

from users.models import User

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

class Command(BaseCommand):
    help = 'Run the Telegram bot'

    def handle(self, *args, **kwargs):
        async def start(update: Update, context: CallbackContext) -> None:
            user = update.message.from_user
            chat_id = update.message.chat_id
            if context.args:
                telegram_token = context.args[0]
                try:
                    user = await sync_to_async(User.objects.filter(telegram_token=telegram_token).first)()
                    if user:
                        user.telegram_chat_id = chat_id
                        await sync_to_async(user.save)()
                        await update.message.reply_text('Ваш Telegram успешно привязан.')
                    else:
                        await update.message.reply_text('Неверный токен.')
                except Exception as e:
                    logging.error(f"Ошибка при связывании Telegram: {e}")
                    await update.message.reply_text('Произошла ошибка при связывании Telegram.')
            else:
                await update.message.reply_text('Токен не передан.')

        application = ApplicationBuilder().token("7003188820:AAGKAivg027k1B4e2V-rRiI-8xdzMseW3OY").read_timeout(20).connect_timeout(20).build()

        application.add_handler(CommandHandler("start", start))

        application.run_polling()

