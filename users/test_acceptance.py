from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import unittest


# LOGIN #

# set up degli oggetti necessari
class TestUser(TestCase):
    def setUp(self):
        # User setup
        self.user = User.objects.create_user(username='studentest1', password='testing321', email='studentest1@test.it')
        self.user.save()
        self.passwordDefault = 'testing321'
        self.user2 = User.objects.create_user(username='studentest2', password='testing321',
                                              email='studentest2@test.it')
        self.user2.save()
        # Client setup
        self.client = Client()

        self.login_data_fail = {
            'username': 'studentest1',
            'password': 'errata'
        }

        self.login_data_ok = {
            'username': 'studentest1',
            'password': 'testing321'
        }

    # REGISTRAZIONE

    # controllo se ho 2 utenti
    def test_count_user_before(self):
        self.assertEquals(len(User.objects.all()), 2)

    # Test sul funzionamento della registrazione, al termine devo avere 3 utenti
    def test_registrazione(self):
        # ok
        response = self.client.post('/register/',
                                    {'username': 'asdsadasd', 'email': 'just@google.it', 'password1': 'testing321',
                                     'password2': 'testing321'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEquals(len(User.objects.all()), 3)

        # not ok, utente già registrato
        response = self.client.post('/register/',
                                    {'username': 'studentest1', 'password1': 'testing321', 'password2': 'testing321',
                                     'email': 'just@google.it'})
        self.assertEqual(response.status_code, 200)
        self.assertEquals(len(User.objects.all()), 3)

    # LOGIN

    def test_login_fail(self):
        response = self.client.post('/login/', self.login_data_fail, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_active)

    def test_login_ok(self):
        response = self.client.post('/login/', self.login_data_ok, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_active)
        self.assertContains(response, '<h1>Direct chats</h1>')

    # LOGOUT #

    def test_logout(self):
        response = self.client.post('/logout/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_active)
        self.assertContains(response, '<legend>You have been logged out!</legend>')




