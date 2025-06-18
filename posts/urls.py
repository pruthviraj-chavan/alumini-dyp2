from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('<int:post_id>/', views.post_detail, name='post_detail'),
    path('create/', views.post_create, name='post_create'),
    path('<int:post_id>/update/', views.post_update, name='post_update'),
    path('<int:post_id>/delete/', views.post_delete, name='post_delete'),
]
