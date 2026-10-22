from django.contrib.auth.models import User
from django.test import TestCase

from .models import UserProfile


class AccountFlowTests(TestCase):
	def test_registration_persists_user_and_logs_them_in(self):
		response = self.client.post('/register/', {
			'username': 'richelle',
			'first_name': 'Richelle',
			'last_name': 'Servando',
			'password': 'A-strong-test-password-42!',
			'password2': 'A-strong-test-password-42!',
		})

		self.assertRedirects(response, '/dashboard/')
		user = User.objects.get(username='richelle')
		self.assertTrue(user.check_password('A-strong-test-password-42!'))
		self.assertTrue(response.wsgi_request.user.is_authenticated)
		self.assertEqual(user.profile.role, UserProfile.Role.STUDENT)

	def test_mismatched_passwords_do_not_create_user(self):
		response = self.client.post('/register/', {
			'username': 'richelle',
			'password': 'A-strong-test-password-42!',
			'password2': 'different-password',
		})

		self.assertEqual(response.status_code, 200)
		self.assertFalse(User.objects.filter(username='richelle').exists())

	def test_login_uses_saved_credentials(self):
		User.objects.create_user(username='richelle', password='A-strong-test-password-42!')

		response = self.client.post('/login/', {
			'username': 'richelle',
			'password': 'A-strong-test-password-42!',
		})

		self.assertRedirects(response, '/dashboard/')

	def test_staff_sees_staff_dashboard(self):
		user = User.objects.create_user(username='staff-user', password='A-strong-test-password-42!')
		UserProfile.objects.create(user=user, role=UserProfile.Role.STAFF)
		self.client.force_login(user)

		response = self.client.get('/dashboard/')

		self.assertContains(response, 'Staff Dashboard')

	def test_superuser_sees_admin_dashboard(self):
		user = User.objects.create_superuser(username='admin-user', password='A-strong-test-password-42!')
		self.client.force_login(user)

		response = self.client.get('/dashboard/')

		self.assertContains(response, 'Admin Dashboard')
