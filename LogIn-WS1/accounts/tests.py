from django.contrib.auth.models import User
from django.test import TestCase


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
