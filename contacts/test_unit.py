from django.test import TestCase, Client
from django.contrib.auth.models import User
from contacts.models import Contact


class TestRubrica(TestCase):
    def setUp(self):
        # User setup
        self.user = User.objects.create_user(username='studentest1', password='testing321', email='studentest1@test.it')
        self.user.save()
        self.passwordDefault = 'testing321'
        self.user2 = User.objects.create_user(username='studentest2', password='testing321',
                                              email='studentest2@test.it')
        self.user2.save()
        self.user3 = User.objects.create_user(username='studentest3', password='testing321',
                                              email='studentest3@test.it')
        self.user3.save()
        # Client setup
        self.client = Client()

        # Rubrica setup
        self.nuovoContatto = Contact.add_this(Contact(), self.user, self.user2)
        self.nuovoContatto2 = Contact.add_this(Contact(), self.user2, self.user3)
        self.nuovoContatto3 = Contact.add_this(Contact(), self.user2, self.user)

    # visualizzazione rubrica
    def test_visualizza_rubrica(self):
        self.assertEquals(len(Contact.objects.filter(owner=self.user2)), 2)  # user 2 deve avere 2 contatti
        self.assertEquals(len(Contact.objects.filter(owner=self.user)), 1)  # user deve avere 1 contatto

    # visualizza contatti aggiungibili
    def test_visualizzaContatti_aggiungibili(self):
        self.assertEquals(len(User.objects.all()) - 1 - Contact.objects.filter(owner=self.user).count(),
                          1)  # user può aggiungere 1 contatto
        self.assertEquals(len(User.objects.all()) - 1 - Contact.objects.filter(owner=self.user2).count(),
                          0)  # user2 non ha contatti aggiungibili

    # test sull'aggiunta di un contatto
    def test_aggiungiContatto(self):
        self.assertEquals(len(Contact.objects.filter(owner=self.user)), 1)  # user deve avere 1 contatto
        Contact.add_this(Contact(), self.user, self.user3)
        self.assertEquals(len(Contact.objects.filter(owner=self.user)), 2)  # user ora deve avere 2 contatti

    # test sulla rimozione di un contatto
    def test_rimuoviContatto(self):
        self.assertEquals(len(Contact.objects.filter(owner=self.user)), 1)  # user deve avere 1 contatto
        Contact.remove_this(Contact(), self.user, self.user2)
        self.assertEquals(len(Contact.objects.filter(owner=self.user)), 0)  # user ora non deve avere contatti


