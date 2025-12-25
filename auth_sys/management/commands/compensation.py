from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from auth_sys.models import CustomUser  # your user model

class Command(BaseCommand):
    help = 'Credit coins to users whose bot_exp is tomorrow or the day after'

    def handle(self, *args, **kwargs):
        today = timezone.now().date()  # just the date part
        tomorrow = today + timedelta(days=1)
        day_after = today + timedelta(days=2)

        # Query users whose bot_exp is tomorrow or day after
        users_to_credit = CustomUser.objects.filter(bot_exp__in=[tomorrow, day_after])

        # Credit coins
        for user in users_to_credit:
            user.coins += 10  # change amount as needed
            user.save()

        self.stdout.write(self.style.SUCCESS(f"Credited {users_to_credit.count()} users."))
