from django.test import TestCase, Client
from django.contrib.auth.models import User
from contacts.models import Contact
from chat.models import PrivateChat, GroupChannel, Partecipa, Message


class TestChat(TestCase):
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

        # Rubrica setup
        self.nuovoContatto = Contact.add_this(Contact(), self.user, self.user2)
        self.nuovoContatto2 = Contact.add_this(Contact(), self.user2, self.user3)
        self.nuovoContatto3 = Contact.add_this(Contact(), self.user2, self.user)

        # Chat privata setup
        self.chat1 = PrivateChat.add_this(PrivateChat(), self.user, self.user2)
        self.chat2 = PrivateChat.add_this(PrivateChat(), self.user2, self.user3)

        # Chat gruppo setup
        self.group1 = GroupChannel.add_this(GroupChannel(), 'Gruppo1')
        self.group2 = GroupChannel.add_this(GroupChannel(), 'Gruppo2')

        # Partecipa setup
        self.partecipa1_1 = Partecipa.add_this(Partecipa(), self.group1, self.user)
        self.partecipa1_2 = Partecipa.add_this(Partecipa(), self.group1, self.user2)
        self.partecipa1_3 = Partecipa.add_this(Partecipa(), self.group1, self.user3)

        self.partecipa2_2 = Partecipa.add_this(Partecipa(), self.group2, self.user)
        self.partecipa2_3 = Partecipa.add_this(Partecipa(), self.group2, self.user3)

        # Messaggi setup
        self.messaggio1_1 = Message.add_this(Message(), self.chat1, self.user, 'Messaggio di prova 1')
        self.messaggio1_2 = Message.add_this(Message(), self.chat1, self.user, 'Messaggio di prova 2')
        self.messaggio2_1 = Message.add_this(Message(), self.chat1, self.user2, 'Messaggio di prova 3')

        self.messaggio2_2 = Message.add_this(Message(), self.chat2, self.user2, 'Messaggio di prova 4')
        self.messaggio3_1 = Message.add_this(Message(), self.chat2, self.user3, 'Messaggio di prova 5')

        self.messaggio1_3 = Message.add_this(Message(), self.group1, self.user, 'Messaggio gruppo 1')
        self.messaggio1_4 = Message.add_this(Message(), self.group1, self.user, 'Messaggio gruppo 2')
        self.messaggio3_2 = Message.add_this(Message(), self.group1, self.user3, 'Messaggio gruppo 3')


    # visualizzazione chat privata
    def test_visualizza_private_chat(self):
        self.assertEquals(len(PrivateChat.objects.filter(participant1=self.user)), 1)  # user deve avere 1 chat da participant1
        self.assertEquals((PrivateChat.objects.filter(participant1=self.user2).count()+PrivateChat.objects.filter(participant2=self.user2).count()), 2)  # user deve avere 2 chat da participant1 e participant2
        self.assertEquals(len(PrivateChat.objects.filter(participant1=self.user3)), 0)  # user3 non deve avere chat da participant1
        self.assertEquals(len(PrivateChat.objects.filter(participant2=self.user3)), 1)  # user3 deve avere 1 chat da participant2

    # visualizzazione chat gruppo
    def test_visualizza_group_chat(self):
        self.assertEquals(len(Partecipa.objects.filter(participant=self.user)), 2)  # user deve avere 2 chat di gruppo
        self.assertEquals(len(Partecipa.objects.filter(participant=self.user2)), 1)  # user2 deve avere 1 chat di gruppo
        self.assertEquals(len(Partecipa.objects.filter(participant=self.user3)), 2)  # user3 deve avere 2 chat di gruppo

    # nuova chat privata
    def test_nuova_private_chat(self):
        self.assertEquals(len(PrivateChat.objects.filter(participant1=self.user)), 1)  # user deve avere 1 chat da participant1
        self.chatTEST = PrivateChat.add_this(PrivateChat(), self.user, self.user3)
        self.assertEquals(len(PrivateChat.objects.filter(participant1=self.user)), 2)  # user deve avere 2 chat da participant1

    # nuova chat gruppo
    def test_nuova_group_chat(self):
        self.assertEquals(len(Partecipa.objects.filter(participant=self.user2)), 1)  # user2 deve avere 1 chat di gruppo
        self.partecipaTEST = Partecipa.add_this(Partecipa(), self.group2, self.user2)
        self.assertEquals(len(Partecipa.objects.filter(participant=self.user2)), 2)  # user2 deve avere 2 chat di gruppo

    # test sull'incremento dell'id chat
    def test_incrementa_id(self):
        self.userTEST = User.objects.create_user(username='studentest4', password='testing321',email='studentest4@test.it')
        self.userTEST.save()

        self.chatTEST = PrivateChat.add_this(PrivateChat(), self.user, self.user3)
        self.chatTEST_inc = PrivateChat.add_this(PrivateChat(), self.user, self.userTEST)
        self.assertEquals(self.chatTEST_inc.id_chat, self.chatTEST.id_chat + 1) # l'id di chatTEST_inc deve essere uguale all'id della chatTEST + 1

    # test visualizzazione messaggi di un utente in una chat
    def test_visualizza_messaggi(self):
        self.assertEquals(len(Message.objects.filter(sender=self.user, chat=self.chat1)), 2) # user ha 2 messaggi nella chat1
        self.assertEquals(len(Message.objects.filter(sender=self.user2, chat=self.chat1)), 1) # user2 ha 1 messaggio nella chat1
        self.assertEquals(len(Message.objects.filter(sender=self.user3, chat=self.chat1)), 0) # user3 non ha messaggio nella chat1

    # test visualizzazione messaggi di una chat privata
    def test_visualizza_messaggi_private_chat(self):
        self.assertEquals(len(Message.objects.filter(chat=self.chat1)), 3) # chat1 ha 3 messaggi
        self.assertEquals(len(Message.objects.filter(chat=self.chat2)), 2) # chat2 ha 2 messaggi

    # test visualizzazione messaggi di una chat di gruppo
    def test_visualizzazione_messaggi_group_chat(self):
        self.assertEquals(len(Message.objects.filter(chat=self.group1)), 3) # group1 ha 3 messaggi
        self.assertEquals(len(Message.objects.filter(chat=self.group2)), 0) # group2 non ha messaggi

    # test aggiunta utente in una chat di gruppo
    def test_aggiunta_utente_gruppo(self):
        self.userTEST = User.objects.create_user(username='studentest4', password='testing321',email='studentest4@test.it')
        self.userTEST.save()

        self.assertEquals(len(Partecipa.objects.filter(group_channel=self.group1)), 3)  # group1 ha 3 partecipanti
        self.partecipaTEST = Partecipa.add_this(Partecipa(), self.group1, self.userTEST)
        self.assertEquals(len(Partecipa.objects.filter(group_channel=self.group1)), 4)  # group1 ha 4 partecipanti

    # test controllo esistenza partecipazione
    def test_controllo_esistenza_partecipazione(self):
        self.assertTrue(Partecipa.check_if_exist(Partecipa(), self.group1, self.user))    # una partecipazione contiene user in group1
        self.assertFalse(Partecipa.check_if_exist(Partecipa(), self.group2, self.user2))    # nessuna partecipazione contiene user2 in group2