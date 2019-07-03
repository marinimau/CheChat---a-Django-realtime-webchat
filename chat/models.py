from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from CheChat import settings
from json import JSONEncoder
from django.db.models import Max

# Create your models here.
AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

# Chat, contiene id e id_ultimo messaggio
class Chat(models.Model):
    id_chat = models.SmallIntegerField('id_chat', default=-1, primary_key=True)

    # assegna come id_chat il valore successivo all'id maggiore
    def counter(self):
        if Chat.objects.count() > 0:
            last_chat = Chat.objects.all().order_by('-id_chat')[0]
            no = last_chat.id_chat
        else:
            no = 0
        return no + 1

# Chat privata, ricorda i 2 partecipanti
class PrivateChat(Chat):
    participant1 = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='participant1',
                                     default='admin')
    participant2 = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='participant2',
                                     default='admin')
    unique_together = (('participant1', 'participant2'),)

    #aggiunge una chat privata
    def add_this(self, user1, user2):
        #controlla se esiste, se non esiste la crea
        if not self.check_if_exist(user1, user2):
            self.id_chat = self.counter()
            self.participant1 = user1
            self.participant2 = user2
            self.save()
            return self
        #se esiste restituisce l'istanza esistente, fa un controllo sulla posizione in cui si trova il nostro user
        else:
            is_user_part1 = len(PrivateChat.objects.all().filter(participant1=user1, participant2=user2))
            if is_user_part1 > 0:
                return PrivateChat.objects.all().get(participant1=user1, participant2=user2)
            else:
                return PrivateChat.objects.all().get(participant1=user2, participant2=user1)

    #controlla se esite una chat privata
    def check_if_exist(self, user1, user2):
        if (PrivateChat.objects.filter(participant1=user1, participant2=user2).count() == 0) and (
                PrivateChat.objects.filter(participant1=user2, participant2=user1).count() == 0):
            return False
        else:
            return True

# Chat di gruppo, ricorda solo il nome del gruppo
class GroupChannel(Chat):
    channel_name = models.CharField('channel_name', max_length=255, default=-1)

    def add_this(self, channel_name):
        self.id_chat = self.counter()
        self.channel_name = channel_name
        self.save()
        return self



# Partecipa, ricorda i partecipanti di ogni gruppo usanso una coppia (gruppo,user)
class Partecipa(models.Model):
    group_channel = models.ForeignKey(GroupChannel, on_delete=models.CASCADE, related_name='group_channel',
                                      default='channel')
    participant = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='participant',
                                    default='admin')
    unique_together = (('group_channel', 'participant'),)

    #aggiunge una tupla in partecipa dato gruppo e user, se non esiste la partecipazione
    def add_this(self, group_channel, user):
        # se non ho la partecipazione
        if not self.check_if_exist(group_channel, user):
            self.group_channel = group_channel
            self.participant = user
            self.save()
        return

    #controlla se esiste una partecipazione
    def check_if_exist(self, group_channel, user):
        if Partecipa.objects.filter(group_channel=group_channel, participant=user).count() == 0:
            return False
        else:
            return True

# Messaggio, ricorda id, mittente, timestamp, testo, chat a cui appartiene
class Message(models.Model):
    id = models.SmallIntegerField('ID', primary_key=True, default=-1)
    sender = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sender')
    timestamp = models.DateTimeField(auto_now_add=True)
    text = models.CharField('text', max_length=255, default="text")
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)

    #restituisce come id da usare per un nuovo messaggio, il numero successivo a quello dell'id piu' grande presente
    def counter(self):
        if Message.objects.count() > 0:
            # -id vuol dire che ordina per id in maniera decrescente
            last_message = Message.objects.all().order_by('-id')[0]
            no = last_message.id
        else:
            no = 0
        return no + 1

    #aggiunge un messaggio data chat, mittente e testo.
    def add_this(self, chat, sender, text):
        self.id = self.counter()
        self.sender = sender
        self.text = text
        self.chat = chat
        self.save()
        return self

