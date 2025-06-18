from django.urls import path
from . import views

urlpatterns = [
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('terms/', views.terms, name='terms'),
    path('directory/', views.directory, name='directory'),
    path('user/<int:user_id>/', views.user_profile, name='user_profile'),
]
