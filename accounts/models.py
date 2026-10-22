from django.conf import settings
from django.db import models


class UserProfile(models.Model):
	class Role(models.TextChoices):
		STUDENT = 'student', 'Student'
		STAFF = 'staff', 'Staff'

	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
	role = models.CharField(max_length=20, choices=Role.choices, default=Role.STUDENT)

	def __str__(self):
		return f'{self.user.username} ({self.get_role_display()})'
