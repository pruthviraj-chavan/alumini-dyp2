from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden

from .models import Post
from .forms import PostForm

@login_required
def post_list(request):
    """View for listing all posts with optional filters"""
    category = request.GET.get('category', '')
    
    # Start with all posts
    posts = Post.objects.all().order_by('-created_at')
    
    # Apply category filter if provided
    if category:
        posts = posts.filter(category=category)
    
    context = {
        'posts': posts,
        'selected_category': category,
    }
    return render(request, 'posts/post_list.html', context)

@login_required
def post_detail(request, post_id):
    """View for displaying a single post"""
    post = get_object_or_404(Post, id=post_id)
    
    context = {
        'post': post,
    }
    return render(request, 'posts/post_detail.html', context)

@login_required
def post_create(request):
    """View for creating a new post"""
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('post_detail', post_id=post.id)
    else:
        form = PostForm()
    
    context = {
        'form': form,
        'action': 'Create',
    }
    return render(request, 'posts/post_form.html', context)

@login_required
def post_update(request, post_id):
    """View for updating an existing post"""
    post = get_object_or_404(Post, id=post_id)
    
    # Check if the user is the author of the post
    if post.user != request.user and not request.user.is_staff:
        return HttpResponseForbidden("You don't have permission to edit this post.")
    
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('post_detail', post_id=post.id)
    else:
        form = PostForm(instance=post)
    
    context = {
        'form': form,
        'post': post,
        'action': 'Update',
    }
    return render(request, 'posts/post_form.html', context)

@login_required
def post_delete(request, post_id):
    """View for deleting a post"""
    post = get_object_or_404(Post, id=post_id)
    
    # Check if the user is the author of the post or an admin
    if post.user != request.user and not request.user.is_staff:
        return HttpResponseForbidden("You don't have permission to delete this post.")
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully!')
        return redirect('post_list')
    
    context = {
        'post': post,
    }
    return render(request, 'posts/post_confirm_delete.html', context)
