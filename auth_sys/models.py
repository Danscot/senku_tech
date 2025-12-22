from django.db import models

from django.contrib.auth.models import AbstractUser

from django.utils import timezone

from datetime import timedelta


class CustomUser(AbstractUser):

    coins = models.PositiveIntegerField(default=0)

    is_prem = models.BooleanField(default=False)

    bot_number = models.CharField(max_length=16, blank=True, null=True)

    bot_exp = models.DateTimeField(blank=True, null=True)

    daily_ad_count = models.PositiveSmallIntegerField(default=0)

    daily_ad_reset = models.DateTimeField(blank=True, null=True)


    def update(self):

        """Call this to refresh user state."""

        self.reset_ads_if_needed()

        # Expire bot if time reached

        if self.bot_exp and timezone.now() >= self.bot_exp:

            self.bot_exp = None

            self.bot_number = None
            
            self.save(update_fields=["bot_exp", "bot_number"])

    def __str__(self):

        return self.username

    def reset_ads_if_needed(self):
        """
        Reset daily ad counter if expiration passed
        """
        if self.daily_ad_reset and timezone.now() >= self.daily_ad_reset:

            self.daily_ad_count = 0

            self.daily_ad_reset = None

            self.save(update_fields=["daily_ad_count", "daily_ad_reset"])

    def add_coins(self, amount=1):
        """
        Add coins ONLY if daily ad limit not reached
        """

        self.reset_ads_if_needed()

        if self.daily_ad_count >= 10:

            return False, "Daily ad limit reached"

        # First ad of the day → set reset timer
        if self.daily_ad_count == 0:

            self.daily_ad_reset = timezone.now() + timedelta(hours=24)

        self.coins += amount

        self.daily_ad_count += 1

        self.save(update_fields=[

            "coins",

            "daily_ad_count",

            "daily_ad_reset"
        ])

        return True, "Coin added"

    def spend_coins(self, amount):

        if self.coins < amount:

            return False

        self.coins -= amount

        self.save(update_fields=["coins"])

        return True


