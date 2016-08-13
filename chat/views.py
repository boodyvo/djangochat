from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from chat.forms import UserCreateForm
from django.contrib.auth import authenticate, logout, login
from django.http import JsonResponse, HttpResponseRedirect
from chat.models import ChatRoom, ChatMessage, IdentUserInChat
from django.utils.crypto import get_random_string
import datetime

def homeView(request):
    if (request.user.is_authenticated()):
        return HttpResponseRedirect('chat/')
    return render(request, 'chat/home.html')

def loginView(request):
    if (request.user.is_authenticated()):
        return HttpResponseRedirect('/chat')
    if (request.method == 'POST'):
        print("Login")
        print(request.POST)
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        print(user)
        if (user is not None):
            if (user.is_active):
                login(request, user)
                print("Ok")
                return HttpResponseRedirect('/chat')
    return render(request, 'chat/login.html')

def signupView(request):
    print("In1")
    if (request.user.is_authenticated()):
        return redirect('../chat/', request)
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        print("In2")
        if form.is_valid():
            user = authenticate(username=request.POST['username'], password=request.POST['password1'])
            print("In3")
            print(user)
            if (user is not None):
                if (user.is_active):
                    print("In4")
                    login(request, user)
                else:
                    print("Not active")
            else:
                print("In5")
                user = User.objects.create_user(request.POST['username'],
                                                request.POST['email'],
                                                request.POST['password1'])
                user.save()
            return chatView(request)
    else:
        form = UserCreateForm()
    print(form)
    return render(request, 'chat/signup.html', {'form': form})

def logoutView(request):
    logout(request)
    return redirect('../', request)

def chatView(request):
    if (request.user.is_authenticated()):
        if (request.method == "POST"):
            try:
                print(request.POST['username'])
                userTo = User.objects.get(username=request.POST['username'])
                if (request.user.id < userTo.id):
                    ChatRoom.objects.create(mainUser=request.user,
                                            secondaryUser=userTo)
                else:
                    ChatRoom.objects.create(mainUser=userTo,
                                            secondaryUser=request.user)
            except:
                userTo = None
            print(userTo)
        user = request.user
        chatArray = []
        chats = ChatRoom.objects.filter(mainUser=user)
        for chat in chats:
            chatArray.append({
                'id': chat.id,
                'username': chat.secondaryUser.username})
        chats = ChatRoom.objects.filter(secondaryUser=user)
        for chat in chats:
            chatArray.append({
                'id': chat.id,
                'username': chat.mainUser.username})
        return render(request, 'chat/chat.html', {'chats': chatArray})
    return HttpResponseRedirect('/')

def chatRoomView(request, chatRoomId):
    if (request.user.is_authenticated()):
        chatRoom = get_object_or_404(ChatRoom, id=chatRoomId)
        if (request.method == "POST"):
            if (request.POST['action'] == "READ_MESSAGE"):
                try:
                    message = ChatMessage.objects.get(id=request.POST['id'])
                    message.read = True
                    message.save()
                    return JsonResponse({'answer': True})
                except:
                    return JsonResponse({'answer': False})
        if (request.user == chatRoom.mainUser or request.user == chatRoom.secondaryUser):
            print(request.user.username)
            userTo = chatRoom.mainUser
            if (request.user == chatRoom.mainUser):
                userTo = chatRoom.secondaryUser
            messages = ChatMessage.objects.filter(chatRoom=chatRoom).extra(order_by=['date'])
            messageArray = []
            for message in messages:
                newMessage = ""
                start = 0
                while(message.message.find('\n', start) > -1):
                    print(newMessage)
                    end = message.message.find('\n', start)
                    newMessage += message.message[start:end] + "<br/>\\\n"
                    start = end + 2
                newMessage += message.message[start:len(message.message)]
                messageArray.append({
                    'id': message.id,
                    'message': newMessage,
                    'author': message.author.username,
                    'read': message.read
                })
            while(True):
                ident = get_random_string(length=32)
                try:
                    isThereChatRoom = IdentUserInChat.objects.get(ident=ident)
                except:
                    isThereChatRoom = None
                if (isThereChatRoom == None):
                    try:
                        IUC = IdentUserInChat.objects.get(user=request.user)
                        IUC = ident
                        IUC.save()
                    except:
                        IdentUserInChat.objects.create(user=request.user,
                                                       ident=ident)
                    break
            return render(request, 'chat/chatRoomBase.html', {'chatId': chatRoomId,
                                                              'user': userTo,
                                                              'messages': messageArray,
                                                              'identifier': ident})
    return HttpResponseRedirect('/')
