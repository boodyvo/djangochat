from channels.channel import Group
from chat.models import ChatRoom, ChatMessage, IdentUserInChat
from django.contrib.auth.models import User
from channels.sessions import channel_session
import datetime
import json

@channel_session
def ws_connect(message):
    print("----------- Connected ----------")
    print(message.content)

@channel_session
def ws_message(message):
    print("----------- Message ------------")
    timeRecieve = datetime.datetime.now()
    data = json.loads(message.content['text'])
    prefix, chatRoomId = message['path'].strip('/').split('/')
    print(chatRoomId)
    if (data['action'] == "INIT"):
        print("Init")
        ident = data['identifier']
        if (ident != None and ident != "" and ident != "None"):
            try:
                identUser = IdentUserInChat.objects.get(ident=ident)
            except:
                identUser = None
            if (identUser != None):
                identUser.ident = ""
                identUser.save()
                message.channel_session['user'] = identUser.user.username
                message.channel_session['room'] = chatRoomId
                Group(message.channel_session['room']).add(message.reply_channel)
                print(message.channel_session['user'])
                print(message.channel_session['room'])
    elif (data['action'] == "SEND_MESSAGE"):
        print("Send")
        try:
            ChatMessage.objects.create(message=data['message'],
                                       author=User.objects.get(username=message.channel_session['user']),
                                       chatRoom=ChatRoom.objects.get(id=message.channel_session['room']),
                                       date=timeRecieve)
            Group(message.channel_session['room']).send({'text': json.dumps({
                "message": data['message'],
                "author": message.channel_session['user'],
                "id": 0,
                "read": False
            })})
        except:
            print("Error with message")

@channel_session
def ws_disconnect(message):
    print("----------- Disconnected -------")
    Group(message.channel_session['room']).discard(message.reply_channel)
