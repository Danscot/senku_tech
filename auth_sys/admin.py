from django.contrib import admin

from django.contrib.auth.admin import UserAdmin

from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):

    model = CustomUser

    fieldsets = UserAdmin.fieldsets + (

        (None, {'fields': ('coins', 'is_prem', 'bot_number', 'bot_exp', 'daily_ad_count', 'daily_ad_reset', 'ver_code', 'email_ver', 'attempts')}),

    )
    add_fieldsets = UserAdmin.add_fieldsets + (
    	
        (None, {'fields': ('coins', 'is_prem', ' bot_number', 'bot_exp', 'daily_ad_count', 'daily_ad_reset', 'ver_code', 'email_ver', 'attempts')}),
    )
