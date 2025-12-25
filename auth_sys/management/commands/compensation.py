from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from auth_sys.models import CustomUser  

class Command(BaseCommand):
    help = 'Credit coins to users whose bot_exp was in the last 24 hours'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        start_time = now - timedelta(days=2)
        end_time = now

        # Query users whose bot_exp is within the last 24 hours
        users_to_credit = CustomUser.objects.filter(bot_exp__gte=start_time, bot_exp__lte=end_time)

        # Credit coins
        for user in users_to_credit:
            user.coins += 10  # change amount as needed
            user.save()

        self.stdout.write(self.style.SUCCESS(f"Credited {users_to_credit.count()} users."))
