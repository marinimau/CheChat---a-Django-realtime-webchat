"""CheChat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from users import views as users_views
from contacts import views as contact_views
from chat import views as chat_views
from CheChat import views as global_views
from django.contrib.auth import views as auth_views

urlpatterns = [
  path('admin/', admin.site.urls),
  path (r'register/',users_views.register, name='register'),
  path ('profile/',chat_views.chat_list, name='profile'),
  path ('group_chat/', chat_views.group_list, name='group_chat'),
  path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
  path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
  path('new_chat/', chat_views.new_chat, name='new_chat'),
  path('new_group_chat/', chat_views.new_group_chat, name='new_group_chat'),
  path('contacts/', contact_views.contacts, name='contacts'),
  path('addable_contacts/', contact_views.addable_contacts, name='addable_contacts'),
  path('add_contact/', contact_views.add_contact, name='add_contact'),
  path('remove_contact/', contact_views.remove_contact, name='remove_contact'),
  path('create_chat/', chat_views.create_chat, name='create_chat'),
  path('create_group/', chat_views.create_group, name='create_group'),
  path('private_chat/', chat_views.private_chat, name='private_chat'),
  path('group_chat_page/', chat_views.goto_groupchat_from_id, name="group_chat_page"),
  path('send_message/', chat_views.send_message, name='send_message'),
  path('add_partecipants/', chat_views.add_partecipants, name='add_partecipants'),
  path('add_users_to_group/', chat_views.add_users_to_group, name='add_users_to_group'),
  path('get_group_chat_messages/', chat_views.get_json_chat_messages, name='get_group_chat_messages'),
  path('get_private_chat_messages/', chat_views.get_json_chat_messages, name='get_private_chat_messages')


]# dentro as view gli dico che deve guardare dentro la cartella users
 # per poter utilizzare l'html corrispondente#