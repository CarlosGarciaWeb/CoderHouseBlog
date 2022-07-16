from django.views.generic import CreateView
from django.contrib.auth.forms import UserChangeForm
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from .models import Post
from django.http import HttpRequest, HttpResponseRedirect
from .forms import PostForm, SignUpForm
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
    'edit_profile': template_path+'edit_profile.html'
}

def Home(request):
    post_data = Post.objects.all().order_by('-blog_date')
    most_likes = max([post.total_likes() for post in post_data])
    most_liked = [post for post in post_data if post.total_likes() == most_likes]
    most_liked = random.choice(most_liked)
    first_post = post_data[len(post_data)-1]
    content = [blogcontent for blogcontent in post_data]
    context = {
        'posts': post_data,
        'first_post': first_post,
        'most_liked': most_liked

    }
    return render(request, template_pages['home'], context=context)


def About(request):
    return render(request, template_pages['about'])


def BlogPost(request, blog_slug):
    post_data = Post.objects.get(slug_post=blog_slug)
    all_post_data = Post.objects.all().order_by('-blog_date')
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
    context = {
        "post": post_data,
        "likes": total_likes,
        "liked": liked,
        'post_featured': new_feature_post
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

def User(request, user):
    return render(request, template_pages['user'])

class UserEditView(CreateView):
    form_class = UserChangeForm
    template_name = template_pages['edit_profile']
    success_url = reverse_lazy('Home')


class AddPostView(CreateView):
    model = Post
    form_class = PostForm
    template_name = template_pages['add_post']
    success_url = reverse_lazy('Home')

    def form_valid(self, form):
        form.instance.user_name = self.request.user
        return super().form_valid(form)

class Registration(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')