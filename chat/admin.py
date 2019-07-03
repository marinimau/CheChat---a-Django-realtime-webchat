from django.contrib import admin
from chat import models

# Register your models here.
admin.site.register(models.Message)
admin.site.register(models.Chat)
admin.site.register(models.GroupChannel)
admin.site.register(models.PrivateChat)
admin.site.register(models.Partecipa)
