from django.core.management.base import BaseCommand
from users.models import User

class Command(BaseCommand):
    help = 'Cleans duplicate telegram tokens in User model'

    def handle(self, *args, **kwargs):
        users = User.objects.all()
        tokens = set()
        duplicates = 0
        for user in users:
            if user.telegram_token in tokens:
                user.telegram_token = None  # или присвойте другое уникальное значение
                user.save()
                duplicates += 1
            else:
                tokens.add(user.telegram_token)

        self.stdout.write(self.style.SUCCESS(f'Successfully cleaned {duplicates} duplicate telegram tokens'))
