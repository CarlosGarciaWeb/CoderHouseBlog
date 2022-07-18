from pydoc_data.topics import topics
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy, reverse
from .models import Post, Topics
from django.http import HttpRequest, HttpResponseRedirect
from .forms import PostForm, SignUpForm, ProfileChangeForm, SearchForm
import os
import random
# Create your views here.

template_path = 'my_blog/'

template_pages = {
    'home': template_path+'index.html',
    'about': template_path+'about.html',
    'blog_post': template_path+'blog_post.html',
    'add_post': template_path+'add_post.html',
    'user': template_path+'user.html',
    'edit_profile': template_path+'edit_profile.html',
    'edit_post': template_path+'edit_post.html',
    'delete_post': template_path+'delete_post.html',
    'search_post': template_path+'search_posts.html'
}

def Home(request):
    post_data = Post.objects.all().order_by('-blog_date')
    most_likes = max([post.total_likes() for post in post_data])
    most_liked = [post for post in post_data if post.total_likes() == most_likes]
    most_liked = random.choice(most_liked)
    first_post = post_data[len(post_data)-1]
    content = [blogcontent for blogcontent in post_data]
    form = SearchForm()
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search_term = form.cleaned_data['search_term']
            return redirect(reverse('search', kwargs={'search_term': search_term}))
            
    context = {
        'posts': post_data,
        'first_post': first_post,
        'most_liked': most_liked,
        'form': form,

    }
    return render(request, template_pages['home'], context=context)


def About(request):
    form = SearchForm(request.POST)
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search_term = form.cleaned_data['search_term']
            return redirect(reverse('search', kwargs={'search_term': search_term}))
    return render(request, template_pages['about'], context={'form': form})


def BlogPost(request, blog_slug):
    post_data = Post.objects.get(slug_post=blog_slug)
    all_post_data = Post.objects.all()
    most_likes = max([post.total_likes() for post in all_post_data])
    most_liked_all = [post for post in all_post_data if post.total_likes() == most_likes]
    most_liked = random.choice(most_liked_all)
    most_liked_index = 0
    updated_post_data_index = 0
    updated_post_data = [post for post in Post.objects.all()]
    new_feature_post = ""
    if most_liked.slug_post == blog_slug:
        most_liked_index = most_liked_all.index(most_liked)
        updated_post_data_index = updated_post_data.index(most_liked)
        most_liked_all.pop(most_liked_index)
        updated_post_data.pop(updated_post_data_index)
        new_feature_post = random.choice(updated_post_data)
    else:
        new_feature_post = most_liked
    
    total_likes = post_data.total_likes()
    liked = False
    if post_data.likes.filter(id=request.user.id).exists():
        liked = True
    form = SearchForm()
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search_term = form.cleaned_data['search_term']
            return redirect(reverse('search', kwargs={'search_term': search_term}))
    context = {
        "post": post_data,
        "likes": total_likes,
        "liked": liked,
        'post_featured': new_feature_post,
        'form': form
    }
    return render(request, template_pages['blog_post'], context=context)


def Like(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    post_slug = post.slug_post
    return HttpResponseRedirect(reverse('blogpost', args=[str(post_slug)]))


def UserView(request, user_name):
    user_id = User.objects.get(username=request.user)
    
    liked_posts = Post.objects.filter(likes=user_id)
    print(liked_posts)

    context = {
        'liked_post_all': liked_posts,        
    }
    return render(request, template_pages['user'], context=context)

class UserEditView(UpdateView):
    form_class = ProfileChangeForm
    template_name = template_pages['edit_profile']
    success_url = reverse_lazy('Home')

    def get_object(self):
        return self.request.user


class AddPostView(CreateView):
    model = Post
    form_class = PostForm
    template_name = template_pages['add_post']
    success_url = reverse_lazy('Home')

    def form_valid(self, form):
        form.instance.user_name = self.request.user
        return super().form_valid(form)

class UpdatePostView(UpdateView):
    model = Post
    template_name = template_pages['edit_post']
    fields = ['title', 'slug_post' ,'blog_meta', 'blog_content', 'topic_tag']


class DeletePostView(DeleteView):
    model = Post
    template_name = template_pages['delete_post']
    success_url = reverse_lazy('Home')




def SearchedPostView(request, search_term):
    print(Post.objects.filter(blog_content__contains="About"))
    all_posts = Post.objects.all()
    post_data = Post.objects.filter(title__contains=search_term) | Post.objects.filter(blog_content__contains=search_term)
    first_post = all_posts[0]
    most_likes = max([post.total_likes() for post in all_posts])
    most_liked = [post for post in all_posts if post.total_likes() == most_likes]
    most_liked = random.choice(most_liked)
    search_found = False
    total_found = len(post_data)
    if len(post_data) > 0:    
        search_found = True
    else:
        search_found = False
    form = SearchForm()
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search_term = form.cleaned_data['search_term']
            return redirect(reverse('search', kwargs={'search_term': search_term}))
    context = {
        'posts': post_data,
        'first_post': first_post,
        'most_liked': most_liked,
        'search_found': search_found,
        'search_term': search_term,
        'total_found': total_found,
        'form': form,
    }
    return render(request, template_pages['search_post'], context=context)

class Registration(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')