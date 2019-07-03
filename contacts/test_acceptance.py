from django.test import TestCase, Client
from django.contrib.auth.models import User
from contacts.models import Contact
from django.contrib.auth import authenticate
import unittest
from django.http import HttpResponse


class TestRubrica(TestCase):
    def setUp(self):
        # User setup
        self.user = User.objects.create_user(username='studentest1', password='testing321', email='studentest1@test.it')
        self.user.save()
        self.passwordDefault = 'testing321'
        self.user2 = User.objects.create_user(username='studentest2', password='testing321',email='studentest2@test.it')
        self.user2.save()
        self.user3 = User.objects.create_user(username='studentest3', password='testing321',email='studentest3@test.it')
        self.user3.save()
        # Client setup
        self.client = Client()



        #mi serve per le pagine login required
        self.login_data_ok = {
            'username': 'studentest1',
            'password': 'testing321'
        }

        self.contact_data = {
            'other_username' : 'studentest2'
        }

    #mi serve perche' le pagine sono tutte @login_required
    def do_login(self):
        response = self.client.post('/login/', self.login_data_ok, follow=True)
        self.assertEqual(response.status_code, 200)



    #--------------------------------------------------------------
    #   VISUALIZZAZIONE PAGINA RUBRICA
    #--------------------------------------------------------------

    # non devo raggiungere la pagina perche' non loggato
    def test_visualizza_rubrica_not_logged(self):
        response = self.client.post('/contacts/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_active)
        self.assertNotContains(response, '<h1>Contacts</h1>') #not Contains


    #raggiungo la pagina correttamente
    def test_visualizza_rubrica_logged(self):
        self.do_login()
        response = self.client.post('/contacts/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_active)
        self.assertContains(response, '<h1>Contacts</h1>')

    # --------------------------------------------------------------
    #   VISUALIZZAZIONE PAGINA ADD CONTACTS
    # --------------------------------------------------------------

    #non sono loggato, non deve raggiungere add contacts
    def test_visualizza_contatti_aggiungibili_not_logged(self):
        response = self.client.post('/addable_contacts/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_active)
        self.assertNotContains(response, '<h1>Add contact</h1>')

    # visualizza contatti aggiungibili
    def test_visualizza_contatti_aggiungibili_logged(self):
        self.do_login()
        response = self.client.post('/addable_contacts/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_active)
        self.assertContains(response, '<h1>Add contact</h1>')

    # --------------------------------------------------------------
    #   AGGIUNTA DI UN CONTATTO
    # --------------------------------------------------------------

    def test_aggiungi_contatto_ok(self):
        n_contacts_before = Contact.objects.count()
        self.do_login()
        response = self.client.post('/add_contact/', self.contact_data, follow=True)
        n_contacts_after = Contact.objects.count()
        self.assertTrue(n_contacts_after > n_contacts_before) #controllo che abbia aggiunto un contatto

    def test_non_duplicazione_contatto(self):
        self.do_login()
        response = self.client.post('/add_contact/', self.contact_data, follow=True) #aggiungo
        n_contacts_before = Contact.objects.count()
        response = self.client.post('/add_contact/', self.contact_data, follow=True) #provo a aggiungere lo stesso
        n_contacts_after = Contact.objects.count()
        self.assertTrue(n_contacts_after==n_contacts_before,) #controllo che non ci siano state aggiunte

    # --------------------------------------------------------------
    #   RIMOZIONE CONTATTO
    # --------------------------------------------------------------

    def test_rimuovi_contatto(self):
        self.do_login()
        response = self.client.post('/add_contact/', self.contact_data, follow=True)  # aggiungo
        n_contacts_before = Contact.objects.count() #salvo il numero
        response = self.client.post('/remove_contact/', self.contact_data, follow=True) #rimuovo
        n_contacts_after = Contact.objects.count() #salvo il numero attuale
        self.assertTrue(n_contacts_before > n_contacts_after) #dovevo avere più contatti prima

