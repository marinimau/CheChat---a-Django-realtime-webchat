from contacts.models import Contact
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

#restituisce la lista degli utenti meno l'utente corrente
def get_other_user(request):
    return (User.objects.all().exclude(username=request.user))

#restituisce i contatti che posso aggiungere, tutti gli user - quelli che ho gia' tra i contatti
def get_addable_users(request):
    return [user for user in get_other_user(request) if user not in get_contacts(request)]

#restituisce la lista dei contatti
def get_contacts(request):
    return ([c.other for c in Contact.objects.all().filter(owner=request.user)])


