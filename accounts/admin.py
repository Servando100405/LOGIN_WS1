from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'account_type', 'created_at')
	list_filter = ('account_type', 'created_at')
	search_fields = ('user__username', 'user__first_name', 'user__last_name')


admin.site.unregister(User)


@admin.register(User)
class StaffUserAdmin(UserAdmin):
	list_display = ('username', 'first_name', 'last_name', 'is_staff', 'is_active')
