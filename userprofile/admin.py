from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
# Register your models here.

from .models import UserProfile

class ProfileInline(admin.StackedInline):
    """定义一个行内admin"""
    model = UserProfile
    can_delete = False
    verbose_name_plural = "用户"

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)

admin.site.unregister(User)
admin.site.register(User,UserAdmin)