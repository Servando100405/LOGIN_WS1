from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
	ACCOUNT_TYPES = (
		('student', 'Student'),
		('teacher', 'Teacher'),
		('staff', 'Staff'),
	)

	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
	account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES, default='student')
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ('-created_at',)

	def __str__(self):
		return f'{self.user.username} ({self.get_account_type_display()})'
