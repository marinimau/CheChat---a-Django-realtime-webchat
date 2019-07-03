from django.test import TestCase, Client
from django.contrib.auth.models import User
from contacts.models import Contact
from chat.models import Chat, PrivateChat, Partecipa, GroupChannel, Message
from django.contrib.auth import authenticate
import unittest
from django.http import HttpResponse


class TestChat(TestCase):
    def setUp(self):
        # User setup
        self.passwordDefault = 'testing321'

        self.user = User.objects.create_user(username='studentest1', password='testing321',
                                             email='studentest1@test.it')
        self.user.save()

        self.user2 = User.objects.create_user(username='studentest2', password='testing321',
                                              email='studentest2@test.it')
        self.user2.save()

        self.user3 = User.objects.create_user(username='studentest3', password='testing321',
                                              email='studentest3@test.it')
        self.user3.save()

        self.user4 = User.objects.create_user(username='studentest4', password='testing321',
                                              email='studentest4@test.it')
        self.user4.save()

        # Client setup
        self.client = Client()

        # mi serve per le pagine login required
        self.login_data_ok = {
            'username': 'studentest1',
            'password': 'testing321'
        }

        # DATI CHAT PRIVATA PRE-CREATA
        self.private_chat = PrivateChat.add_this(PrivateChat(), self.user, self.user2)
        self.privata_chat_data = {
            'id_chat': self.private_chat.id_chat
        }

        # DATI CHAT DI GRUPPO PRE-CREATA
        self.group_chat = GroupChannel.add_this(GroupChannel(), 'CanaleTest')
        Partecipa.add_this(Partecipa(), self.group_chat, self.user)
        Partecipa.add_this(Partecipa(), self.group_chat, self.user2)

        self.group_chat_data = {
            'id_chat': self.group_chat.id_chat
        }

        self.new_private_chat_data = {
            'other_username': self.user3.username
        }

        self.new_group_chat_data = {
            'participants': [self.user2.username, self.user3.username],
            'chat_name_input': 'nuovo gruppo'
        }

        self.add_participants_data = {
            'group_id': self.group_chat.id_chat,
            'participants': [self.user4.username]
        }

        self.message1 = Message.add_this(Message(), self.private_chat, self.user,
                                         'corpo del messaggio test chat privata')
        self.message2 = Message.add_this(Message(), self.group_chat, self.user,
                                         'corpo del messaggio test chat di gruppo')

        self.message_data_private_chat = {
            'text-message-input': 'generato durante il test di invio',
            'id_chat': self.private_chat.id_chat
        }

        self.message_data_group_chat = {
            'text-message-input': 'generato durante il test di invio',
            'id_chat': self.group_chat.id_chat
        }

    # mi serve perché le pagine sono tutte @login_required
    def do_login(self):
        response = self.client.post('/login/', self.login_data_ok, follow=True)
        self.assertEqual(response.status_code, 200)

    # --------------------------------------------------------------
    #
    #
    #   CONTROLLI SULLA PROTEZIONE DELLE PAGINE LOGIN_REQUIRED
    #
    #   -tutti i test devono riuscire se siamo loggati e fallire altrimenti
    # --------------------------------------------------------------
    # --------------------------------------------------------------
    #   VISUALIZZAZIONE PAGINA LISTA CHAT PRIVATE
    # --------------------------------------------------------------

    # non devo raggiungere la pagina perche' non loggato
    def test_visualizza_lista_chat_private_not_logged(self):
        response = self.client.post('/profile/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_active)
        self.assertNotContains(response, '<h1>Direct chats</h1>')  # not Contains

    # raggiungo la pagina correttamente
    def test_visualizza_lista_chat_private_logged(self):
        self.do_login()
        response = self.client.post('/profile/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_active)
        self.assertContains(response, '<h1>Direct chats</h1>')  # Contains

    # --------------------------------------------------------------
    #   VISUALIZZAZIONE VISUALIZZAZIONE PAGINA CHAT DI GRUPPO
    # --------------------------------------------------------------

    # non raggiungo
    def test_visualizza_lista_chat_gruppo_not_logged(self):
        response = self.client.post('/group_chat/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_active)
        self.assertNotContains(response, '<h1>Group chats</h1>')  # not Contains

    # raggiungo la pagina correttamente
    def test_visualizza_lista_chat_gruppo_logged(self):
        self.do_login()
        response = self.client.post('/group_chat/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_active)
        self.assertContains(response, '<h1>Group chats</h1>')  # Contains

    # --------------------------------------------------------------
    #   VISUALIZZAZIONE PAGINA CONVERSAZIONE PRIVATA
    # --------------------------------------------------------------

    # non raggiungo la pagina
    def test_visualizza_singola_chat_privata_not_logged(self):
        response = self.client.post('/private_chat/', self.privata_chat_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_active)
        self.assertNotContains(response, 'To:studentest2')  # Not contains

    # raggiungo la pagina correttamente
    def test_visualizza_singola_chat_privata_logged(self):
        self.do_login()
        response = self.client.post('/private_chat/', self.privata_chat_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_active)
        self.assertContains(response, 'To:studentest2')  # Contains

    # --------------------------------------------------------------
    #   VISUALIZZAZIONE PAGINA CONVERSAZIONE DI GRUPPO
    # --------------------------------------------------------------

    # non raggiungo la pagina
    def test_visualizza_chat_group_not_logged(self):
        response = self.client.post('/group_chat_page/', self.group_chat_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_active)
        self.assertNotContains(response, 'CanaleTest')  # Not contains

    # raggiungo la pagina correttamente
    def test_visualizza_chat_group_logged(self):
        self.do_login()
        response = self.client.post('/group_chat_page/', self.group_chat_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_active)
        self.assertContains(response, 'CanaleTest')  # Contains

    # --------------------------------------------------------------
    #   VISUALIZZAZIONE PAGINA NUOVA CHAT PRIVATA
    # --------------------------------------------------------------

    # non raggiungo la pagina
    def test_visualizza_new_chat_page_not_logged(self):
        response = self.client.post('/new_chat/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_active)
        self.assertNotContains(response, 'New private chat')  # Not contains

    # raggiungo la pagina correttamente
    def test_visualizza_new_chat_page_logged(self):
        self.do_login()
        response = self.client.post('/new_chat/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_active)
        self.assertContains(response, 'New private chat')  # Contains

    # --------------------------------------------------------------
    #   VISUALIZZAZIONE PAGINA NUOVA CHAT DI GRUPPO
    # --------------------------------------------------------------

    # non raggiungo la pagina
    def test_visualizza_new_group_chat_page_not_logged(self):
        response = self.client.post('/new_group_chat/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_active)
        self.assertNotContains(response, 'New group chat')  # Not contains

    # raggiungo la pagina correttamente
    def test_visualizza_new_group_chat_page_logged(self):
        self.do_login()
        response = self.client.post('/new_group_chat/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_active)
        self.assertContains(response, 'New group chat')  # Contains

    # --------------------------------------------------------------
    #   VISUALIZZAZIONE PAGINA AGGIUNGI PARTECIPANTI ALLA CHAT DI GRUPPO
    # --------------------------------------------------------------

    # non raggiungo la pagina
    def test_add_users_to_group_not_logged(self):
        response = self.client.post('/add_partecipants/', self.group_chat_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_active)
        self.assertNotContains(response, 'Add users to group chat')  # Not contains

        # raggiungo la pagina correttamente

    def test_add_users_to_group_logged(self):
        self.do_login()
        response = self.client.post('/add_partecipants/', self.group_chat_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_active)
        self.assertContains(response, 'Add users to group chat')  # Contains

    # --------------------------------------------------------------
    #
    #
    #   CONTROLLI SULLA CREAZIONE DELLA CHAT PRIVATA
    #
    #
    # --------------------------------------------------------------
    def test_nuova_chat_privata(self):
        self.do_login()
        n_private_chat_before = Chat.objects.count()
        response = self.client.post('/create_chat/', self.new_private_chat_data, follow=True)
        n_private_chat_after = Chat.objects.count()
        self.assertTrue(n_private_chat_after > n_private_chat_before)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_active)
        self.assertContains(response, 'To:studentest3')  # Ci reindirizza alla chat appena creata

    def test_duplicazione_chat(self):
        self.do_login()
        response = self.client.post('/create_chat/', self.new_private_chat_data, follow=True)
        n_chat_before = Chat.objects.count()
        response1 = self.client.post('/create_chat/', self.new_private_chat_data, follow=True)
        n_chat_after = Chat.objects.count()
        self.assertTrue(n_chat_after == n_chat_before)  # Non crea la chat in quanto già esistente
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_active)
        self.assertContains(response, 'To:studentest3')  # Tuttavia mi reindirizza a quella già esistente

    # --------------------------------------------------------------
    #
    #
    #   CONTROLLI SULLA CREAZIONE DELLA CHAT DI GRUPPO
    #
    #
    # --------------------------------------------------------------
    def test_nuova_chat_gruppo(self):
        self.do_login()
        n_chat_before = Chat.objects.count()
        response = self.client.post('/create_group/', self.new_group_chat_data, follow=True)
        n_chat_after = Chat.objects.count()
        self.assertTrue(n_chat_after > n_chat_before)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_active)
        self.assertContains(response, 'nuovo gruppo')  # Ci reindirizza alla chat appena creata

    # --------------------------------------------------------------
    #
    #
    #   CONTROLLI SULL'AGGIUNTA DI PARTECIPANTI
    #
    #
    # --------------------------------------------------------------
    def test_aggiungi_partecipanti(self):
        self.do_login()
        n_partecipants_before = Partecipa.objects.all().filter(group_channel=self.group_chat).count()
        response = self.client.post('/add_users_to_group/', self.add_participants_data, follow=True)
        n_partecipants_after = Partecipa.objects.all().filter(group_channel=self.group_chat).count()
        self.assertTrue(n_partecipants_after > n_partecipants_before)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_active)
        self.assertContains(response, 'CanaleTest')  # Ci reindirizza al gruppo a cui è stato aggiunto user4

    # --------------------------------------------------------------
    #
    #
    #   CONTROLLI SULLA VISUALIZZAZIONE/INVIO DEI MESSAGGI
    #
    #
    # --------------------------------------------------------------
    def test_visualizzazione_messaggio_chat_privata(self):
        self.do_login()
        response = self.client.post('/private_chat/', self.privata_chat_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_active)
        self.assertContains(response, 'corpo del messaggio test chat privata')  # Contains


    def test_visualizzazione_messaggio_chat_gruppo(self):
        self.do_login()
        response = self.client.post('/group_chat_page/', self.group_chat_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_active)
        self.assertContains(response, 'corpo del messaggio test chat di gruppo')  # Contains

    def test_invio_messaggio_chat_privata(self):
        self.do_login()
        invio = self.client.post('/send_message/', self.message_data_private_chat, follow=True)
        response = self.client.post('/private_chat/', self.privata_chat_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_active)
        self.assertContains(response, 'generato durante il test di invio')  # Contains

    def test_invio_messaggio_chat_gruppo(self):
        self.do_login()
        invio = self.client.post('/send_message/', self.message_data_group_chat, follow=True)
        response = self.client.post('/group_chat_page/', self.group_chat_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_active)
        self.assertContains(response, 'corpo del messaggio test chat di gruppo')  # Contains

