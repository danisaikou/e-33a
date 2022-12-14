from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView
import json

from .models import User, Post, Profile
from .forms import PostForm, ProfileForm



def index(request):
    # Create new post when request is POST (ha)
    if request.method == 'POST':
        return create_post(request)

    # The form to create a new post 
    form = PostForm()
    # Pagination
    posts = Post.objects.all().order_by('-datetime')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    

    return render(request, 'network/index.html', {
        'posts': posts,
        'form': form, 
        'page_obj': page_obj, 
        'page_number': page_number, 
    })

@login_required 
def create_post(request):
    # Create new post when request is POST (ha)
    if request.method == 'POST':
        form = PostForm(request.POST or None)

        # Confirm validity before proceeding
        if form.is_valid:
            post = form.save(commit=False)
            post.user_id = request.user
            post.save()

            return redirect('index')

@login_required
def like(request, pk):
    # I know this isn't working properly but if I remove it things break worse for some reason
    try:
        likes = None
        post = Post.objects.get(id = pk)
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            likes = False
        else: 
            post.likes.add(request.user)
            likes = True
        return JsonResponse({
            'count': post.total_likes(),
            'likes': likes 
        })
    except: 
        return JsonResponse({'message': 'Error'}, status = 400)

@login_required
def profile(request, pk):
    
    # Get username, following/follower counts, and posts from just the user 
    user = request.user
    profile = User.objects.get(id=pk)
    posts = Post.objects.filter(user_id=user).order_by('-datetime')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    form = ProfileForm()
    
    return render(request, 'network/profile.html', {
        'posts': posts,
        'page_obj': page_obj, 
        'page_number': page_number,
        'form': form,
        'profile': profile
    })

class edit_profile(UpdateView):
    model = User
    template_name = 'network/edit_profile.html'
    fields = ['first_name', 'last_name',]
    def get_success_url(self):
        return reverse('profile')

class edit_post(UpdateView):
    model = Post
    template_name = 'network/edit_post.html'
    fields = ['content',]
    def get_success_url(self):
        return reverse('index')

@login_required
def follow(request, id):
    if request.method == "POST":
        profile = Profile.objects.get(id=id)
        following = request.user.following
        if profile in following.all():
            following.remove(profile)
        else: 
            following.add(profile)
    return HttpResponseRedirect(reverse('profile', kwargs={
        'id':id
    }))

def following(request):
    return render(request, "network/following.html", {
        'following': request.user.following.all(),
    })



# Everything below this was pre-populated, not created by me
def login_view(request):
    if request.method == 'POST':

        # Attempt to sign user in
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'network/login.html', {
                'message': 'Invalid username and/or password.'
            })
    else:
        return render(request, 'network/login.html')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']

        # Ensure password matches confirmation
        password = request.POST['password']
        confirmation = request.POST['confirmation']
        if password != confirmation:
            return render(request, 'network/register.html', {
                'message': 'Passwords must match.'
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, 'network/register.html', {
                'message': 'Username already taken.'
            })
        login(request, user)
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, 'network/register.html')
