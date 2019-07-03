from contacts.models import Contact
from django.db import models
from django.db.models import Count
from django.conf import settings
from django.contrib.auth.models import User
from chat.models import Chat, PrivateChat, Partecipa, GroupChannel, Message
from contacts import utility_functions as contacts_utility_function


# controlla fra tutte le chat private nel sistema e restituisce quelle in cui l'user corrente
# è presente come primo o secondo partecipante
def get_user_private_chats(request):
    user_in_p1 = PrivateChat.objects.all().filter(participant1=request.user)
    user_in_p2 = PrivateChat.objects.all().filter(participant2=request.user)
    return user_in_p1 | user_in_p2


# restituisce tutti i gruppi per i quali abbiamo una partecipazione dell'utente corrente
def get_user_group_chats(request):
    user_groups = Partecipa.objects.all().filter(participant=request.user)
    return [partecipa.group_channel for partecipa in user_groups]


# restituisce gli utenti con cui posso avere una chat privata.
def get_addable_users_private_chat(request):
    contacts = [user for user in contacts_utility_function.get_contacts(request)]
    return contacts

#restituisce gli utenti presenti nei contatti che ancora non ho aggiunto a un dato gruppo
#viene usata per aggiungere utenti a un gruppo già esistente
def get_addable_user_group_chat(request, chat_id):
    group = GroupChannel.objects.get(id_chat=chat_id)
    partecipazioni_query = Partecipa.objects.filter(group_channel=group)
    partecipazioni = [partecipa for partecipa in partecipazioni_query]
    partecipants = [partecipante.participant for partecipante in partecipazioni]
    contacts = contacts_utility_function.get_contacts(request)
    return [user for user in contacts if user not in partecipants]

# restituisce la lista di partecipanti di un dato gruppo
def get_group_chat_partecipants(request, chat_id):
    group = GroupChannel.objects.get(id_chat=chat_id)
    partecipazioni_query = Partecipa.objects.filter(group_channel=group)
    partecipazioni = [partecipa for partecipa in partecipazioni_query]
    partecipants = [partecipante.participant for partecipante in partecipazioni]
    return partecipants