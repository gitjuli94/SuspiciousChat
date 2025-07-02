from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("forum/", views.forum, name="forum"),
    path('new_chat/', views.new_chat, name='new_chat'),
    path('send_chat/', views.send_chat, name='send_chat'),
    path('delete_chat/', views.delete_chat, name='delete_chat'),
    #path('delete_chat/<int:message_id>/', views.delete_chat, name='delete_chat'),
    path('logout/', views.logout_view, name='logout'),
]
