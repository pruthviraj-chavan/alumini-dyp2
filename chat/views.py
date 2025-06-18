from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db.models import Q

from .models import Message
from .forms import MessageForm

User = get_user_model()

@login_required
def inbox(request):
    """View for displaying user's chat inbox"""
    # Get all users that the current user has chatted with
    chat_partners = User.objects.filter(
        Q(sent_messages__receiver=request.user) | Q(received_messages__sender=request.user)
    ).distinct()
    
    context = {
        'chat_partners': chat_partners,
    }
    return render(request, 'chat/inbox.html', context)

@login_required
def chat_with_user(request, user_id):
    """View for chatting with a specific user"""
    chat_partner = get_object_or_404(User, id=user_id)
    
    # Get all messages between the current user and the chat partner
    messages_list = Message.objects.filter(
        (Q(sender=request.user) & Q(receiver=chat_partner)) | 
        (Q(sender=chat_partner) & Q(receiver=request.user))
    ).order_by('timestamp')
    
    # Mark all received messages as read
    unread_messages = messages_list.filter(receiver=request.user, is_read=False)
    unread_messages.update(is_read=True)
    
    # Handle new message form
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = chat_partner
            message.save()
            return redirect('chat_with_user', user_id=user_id)
    else:
        form = MessageForm()
    
    context = {
        'chat_partner': chat_partner,
        'messages': messages_list,
        'form': form,
    }
    return render(request, 'chat/chat.html', context)

@login_required
def start_new_chat(request):
    """View for starting a new chat with a user"""
    # Get role-based filter
    role_filter = None
    if request.user.role == 'STUDENT':
        role_filter = 'ALUMNI'
    elif request.user.role == 'ALUMNI':
        role_filter = 'STUDENT'
    
    # Get all verified users of the appropriate role that the user can chat with
    if role_filter:
        available_users = User.objects.filter(role=role_filter, is_verified=True)
    else:
        available_users = User.objects.filter(is_verified=True).exclude(id=request.user.id)
    
    context = {
        'available_users': available_users,
    }
    return render(request, 'chat/new_chat.html', context)
