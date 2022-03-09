from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from user_accounts.models import User

class Users(UserAdmin):
    pass
admin.site.register(User, Users)