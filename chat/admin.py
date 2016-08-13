from django.contrib import admin
from chat.models import ChatMessage, ChatRoom
# Register your models here.

admin.site.register([ChatMessage, ChatRoom])