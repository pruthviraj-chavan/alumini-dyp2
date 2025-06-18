from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from .forms import UserRegistrationForm, UserLoginForm, VerificationRequestForm, UserProfileUpdateForm
from .models import VerificationRequest

def register(request):
    """View for user registration"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

def user_login(request):
    """View for user login"""
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                # Check if user is verified
                if user.is_verified or user.is_staff or user.is_superuser:
                    login(request, user)
                    messages.success(request, f'Welcome back, {user.first_name}!')
                    return redirect('home')
                else:
                    # User is not verified
                    messages.error(request, 'Your account is pending verification. Please wait for admin approval.')
                    
                    # Check if user has a pending verification request
                    if not VerificationRequest.objects.filter(student=user, status='PENDING').exists():
                        messages.info(request, 'You can submit a verification request from your profile page after logging in as an unverified user.')
                        # Allow login but with limited access
                        login(request, user)
                        return redirect('request_verification')
            else:
                messages.error(request, 'Invalid email or password.')
    else:
        form = UserLoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def profile(request):
    """View for user profile"""
    if request.method == 'POST':
        form = UserProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        form = UserProfileUpdateForm(instance=request.user)
    
    # Check if user has a pending verification request
    has_pending_request = False
    if request.user.role == 'STUDENT':
        has_pending_request = VerificationRequest.objects.filter(
            student=request.user, 
            status='PENDING'
        ).exists()
    
    context = {
        'form': form,
        'has_pending_request': has_pending_request,
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def request_verification(request):
    """View for students to request verification"""
    # Only students can request verification
    if request.user.role != 'STUDENT':
        messages.error(request, 'Only students can request verification.')
        return redirect('profile')
    
    # Check if user already has a pending request
    if VerificationRequest.objects.filter(student=request.user, status='PENDING').exists():
        messages.info(request, 'You already have a pending verification request.')
        return redirect('profile')
    
    if request.method == 'POST':
        form = VerificationRequestForm(request.POST, request.FILES)
        if form.is_valid():
            verification_request = form.save(commit=False)
            verification_request.student = request.user
            verification_request.save()
            messages.success(request, 'Verification request submitted successfully. Please wait for admin approval.')
            return redirect('profile')
    else:
        form = VerificationRequestForm()
    
    return render(request, 'accounts/request_verification.html', {'form': form})
