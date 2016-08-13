from django.contrib.auth.models import User
from django.db import models


class ChatMessage(models.Model):
    message = models.TextField()
    author = models.ForeignKey(User)
    read = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now=False)
    chatRoom = models.ForeignKey('ChatRoom')

class ChatRoom(models.Model):
    mainUser = models.ForeignKey(User, related_name='mainUser', default=None)
    secondaryUser = models.ForeignKey(User, related_name='secondaryUser', default=None)

    class Meta:
        unique_together = ('mainUser', 'secondaryUser')

class IdentUserInChat(models.Model):
    user = models.ForeignKey(User, default=None)
    ident = models.TextField(default="")
