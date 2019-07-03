from django.db import models
from django.conf import settings

# Create your models here.
AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

# Contact,  tupla (proprietario,altro_utente) usa questa gerarchia cosi' posso avere un contatto senza che lui abbia me
class Contact(models.Model):
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owner')
    other = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='other')

    #aggiunge un contatto dato proprietario e altro utente
    def add_this(self, own, oth):
        self.owner = own
        self.other = oth
        self.save()
        return

    #rimuove un contatto dato proprietario e altro utente
    def remove_this(self, own,oth):
        Contact.objects.filter(owner=own).filter(other=oth).delete()
        return