from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db.models import Q
from posts.models import Post

User = get_user_model()

def home(request):
    """Home page view"""
    # Get recent posts for the home page
    recent_posts = Post.objects.all().order_by('-created_at')[:5]
    
    context = {
        'recent_posts': recent_posts,
    }
    return render(request, 'core/home.html', context)

def about(request):
    """About page view"""
    return render(request, 'core/about.html')

def contact(request):
    """Contact page view"""
    return render(request, 'core/contact.html')

def terms(request):
    """Terms and privacy page view"""
    return render(request, 'core/terms.html')

@login_required
def directory(request):
    """Directory page view with filters"""
    # Get query parameters for filtering
    role = request.GET.get('role', '')
    branch = request.GET.get('branch', '')
    year = request.GET.get('year', '')
    search = request.GET.get('search', '')
    
    # Start with all verified users
    users = User.objects.filter(is_verified=True)
    
    # Always include the current user if they are verified
    if request.user.is_verified and request.user not in users:
        # Create a combined queryset with the current user and other filtered users
        current_user_qs = User.objects.filter(id=request.user.id)
        users = current_user_qs | users
    
    # Apply filters
    if role:
        users = users.filter(role=role)
    if branch:
        users = users.filter(branch=branch)
    if year and year.isdigit():
        users = users.filter(year=int(year))
    if search:
        users = users.filter(
            Q(first_name__icontains=search) | 
            Q(last_name__icontains=search) | 
            Q(email__icontains=search) | 
            Q(branch__icontains=search)
        )
    
    # Get unique branches and years for filter dropdowns
    branches = User.objects.filter(is_verified=True).values_list('branch', flat=True).distinct()
    years = User.objects.filter(is_verified=True).values_list('year', flat=True).distinct()
    
    context = {
        'users': users,
        'branches': branches,
        'years': years,
        'selected_role': role,
        'selected_branch': branch,
        'selected_year': year,
        'search': search,
    }
    return render(request, 'core/directory.html', context)

@login_required
def user_profile(request, user_id):
    """View for displaying user profile"""
    profile_user = get_object_or_404(User, id=user_id)
    
    # Check if the current user is a verified student to show contact info
    show_contact_info = request.user.is_verified and request.user.role == 'STUDENT'
    
    # Get user's posts
    posts = Post.objects.filter(user=profile_user).order_by('-created_at')
    
    context = {
        'profile_user': profile_user,
        'show_contact_info': show_contact_info,
        'posts': posts,
    }
    return render(request, 'core/user_profile.html', context)
