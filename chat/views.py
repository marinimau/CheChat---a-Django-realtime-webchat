from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from chat import utility_functions as chat_utility_functions
from django.contrib.auth.models import User
from chat.models import Chat, Partecipa, PrivateChat, GroupChannel, Message
from django.http import HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
import json
from django.db.models import Max
from contacts import utility_functions as contacts_utility_functions


# restituisce la lista di chat private dell'utente corrente
@login_required()
def chat_list(request):
    chat_list = chat_utility_functions.get_user_private_chats(request)
    return render(request, 'private-chat-list.html',
                  {'private_chats': chat_list, 'len_chats': len(chat_list)})

#restituisce la lista delle chat di gruppo dell'utente corrente
@login_required()
def group_list(request):
    group_list = chat_utility_functions.get_user_group_chats(request)
    return render(request, 'group-chat-list.html', {'group_chats': group_list, 'len_chats': len(group_list)})

#ci porta alla pagina per creare (o continuare) una chat privata, genera la lista di utenti con cui posso chattare
@login_required()
def new_chat(request):
    addable = chat_utility_functions.get_addable_users_private_chat(request)
    return render(request, 'new-chat.html', {'users': addable, 'len_addable': len(addable)})

# Ci porta alla pagina per creare una nuova chat di gruppo, visto che il gruppo non e' stato ancora creato,
# posso aggiungere tutti gli utenti che ho tra i contatti, quindi uso la stessa lista data per la chat privata.
@login_required()
def new_group_chat(request):
    addable = chat_utility_functions.get_addable_users_private_chat(request)
    return render(request, 'new-group-chat.html', {'users': addable, 'len_addable': len(addable)})


# Genera una chat privata tra luser corrente e un altro dato partecipante, ci reindirizza direttamente alla pagina della chat.
@login_required
def create_chat(request):
    other_username = request.POST.get("other_username")
    other_user = User.objects.get(username=other_username)
    private_chat = PrivateChat()
    new_chat = PrivateChat.add_this(private_chat, request.user, other_user)
    messages = Message.objects.all().filter(chat=new_chat)
    return render(request, 'chat.html', {'user2': other_user, 'id_chat': new_chat.id_chat, 'messages': messages})


# Genera una chat di gruppo con l'utente corrente e una data lista di partecipanti presa in input
def create_group(request):
    user_list = request.POST.getlist('participants')
    channel_name = request.POST.get("chat_name_input")
    # se non ho impostato un nome al canale ne metto uno di default
    if len(channel_name) == 0:
        channel_name = "Default name"
    # creo il gruppo
    group_channel = GroupChannel()
    new_chat = GroupChannel.add_this(group_channel, channel_name)
    # creo le tuple in partecipa per ricordare i partecipanti al gruppo
    create_partecipa(request, new_chat, user_list)
    return group_chat(request, new_chat)  # redirect alla pagina della chat di gruppo


# Crea le tuple (chat - utente) in partecipa, per l'utente corrente e per una data lista di utenti
@login_required
def create_partecipa(request, chat, participants_list):
    # aggiunge l'utente corrente
    Partecipa.add_this(Partecipa(), chat, request.user)
    # aggiunge tutti gli utenti presenti nella lista di partecipanti
    for user in participants_list:
        Partecipa.add_this(Partecipa(), chat, (User.objects.all().get(username=user)))
    return

#ci riporta alla pagina della chat privata dopo aver recuperato i messaggi
@login_required
def private_chat(request):
    chat_id = request.POST.get("id_chat")
    chat = PrivateChat.objects.get(id_chat=chat_id)
    messages = Message.objects.all().filter(chat=chat)
    if chat.participant1 == request.user:
        participant = chat.participant2
    else:
        participant = chat.participant1
    return render(request, 'chat.html', {'user2': participant, 'id_chat': chat_id, 'messages': messages})


# trova una chat di gruppo dato l'id e chiama la funzione per generarne la pagina
@login_required
def goto_groupchat_from_id(request):
    chat_id = request.POST.get("id_chat")
    chat = GroupChannel.objects.get(id_chat=chat_id)
    return group_chat(request, chat)

# presa una chat di gruppo, recupera i messaggi e i partecipanti e ci reindirizza alla sua pagina
@login_required
def group_chat(request, chat):
    messages = Message.objects.all().filter(chat=chat)
    partecipants = chat_utility_functions.get_group_chat_partecipants(request, chat.id_chat)
    return render(request, 'group-chat.html', {'group_chat': chat, 'messages': messages, 'partecipants': partecipants})

# invia un messaggio dati in input i suoi campi. Funziona sia per chat privata che di gruppo visto che e' il messaggio
# che ricorda la chat alla quale appartiene.
@login_required
def send_message(request):
    chat_id = request.POST.get("id_chat")
    chat = Chat.objects.get(id_chat=chat_id)
    text_message = request.POST.get("text-message-input")
    if len(text_message) > 0:
        messaggio=Message.add_this(Message(), chat, request.user, text_message)
    response = HttpResponse("200")
    return response

# recupera un messaggio dato il suo id
@login_required
def get_message_by_id(id):
    return Message.objects.all().get(id=id)


# genera la lista di partecipanti che possiamo aggiungere a un dato gruppo
@login_required
def add_partecipants(request):
    chat_id = request.POST.get("id_chat")
    group = GroupChannel.objects.get(id_chat=chat_id)
    partecipanti = chat_utility_functions.get_addable_user_group_chat(request, chat_id)
    return render(request, 'add_users_group_chat.html', {'users': partecipanti, 'len_addable': len(partecipanti),
                                                         'group': group})

# svolge materialmente l'aggiunta degli utenti creando le tuple in partecipa
def add_users_to_group(request):
    user_list = request.POST.getlist('participants')
    group_id = request.POST.get("group_id")
    group = GroupChannel.objects.get(id_chat=group_id)
    create_partecipa(request, group, user_list)
    return group_chat(request, group)  # redirect alla chat di gruppo

#restituisce i messaggi di una chat (singola o privata), in json, serve per il refresh ajax
def get_json_chat_messages(request):
    id_chat = request.POST.get("id_chat")
    chat = Chat.objects.get(id_chat=id_chat)
    messaggi_query = Message.objects.all().filter(chat=chat)
    messaggi_json_array = []
    for messaggio in messaggi_query:
        msg = {'username': messaggio.sender.username, 'text': messaggio.text,
               'timestamp': messaggio.timestamp.strftime('%Y-%m-%d %H:%M')}
        messaggi_json_array.append(msg)
    return JsonResponse(messaggi_json_array, safe=False)