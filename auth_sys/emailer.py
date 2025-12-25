
import random

from django.core.mail import send_mail

from django.conf import settings

class Email:

    def __init__(self, code, email):

        self.code = code

        self.email = email

    def send_verification_code(self):
        """
        Generates and sends a 6-digit verification code
        Returns the code so you can store it in DB or cache
        """
        subject = "Your Verification Code"

        message = f"""
    𝐻𝑒𝓁𝓁𝑜 𝒲𝑜𝓇𝓁𝒹

    Your verification code is:

    {self.code}

    This code expires in 10 minutes.
    If you didn’t request this, ignore this email.

    — BotHost Team
    """

        send_mail(

            subject=subject,

            message=message,

            from_email=settings.DEFAULT_FROM_EMAIL,

            recipient_list=[self.email],

            fail_silently=False,
        )

