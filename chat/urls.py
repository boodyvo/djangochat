from django.conf.urls import url
from django.contrib import admin
from chat import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.homeView, name='chat'),
    url(r'^login/$', views.loginView, name='login'),
    url(r'^signup/$', views.signupView, name='signup'),
    url(r'^logout/$', views.logoutView, name='logout'),
    url(r'^chat/$', views.chatView, name='chat'),
    url(r'^chat/(?P<chatRoomId>[0-9]+)$', views.chatRoomView, name='chatRoom')
]
