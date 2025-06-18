from django.urls import path
from . import views

urlpatterns = [
    path('', views.inbox, name='inbox'),
    path('new/', views.start_new_chat, name='start_new_chat'),
    path('<int:user_id>/', views.chat_with_user, name='chat_with_user'),
]
