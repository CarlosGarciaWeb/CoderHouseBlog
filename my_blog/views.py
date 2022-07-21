from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy, reverse
from .models import Post, Topics, UserProfile, Comments
from django.http import  HttpResponseRedirect
from .forms import PostForm, SignUpForm, ProfileChangeForm, SearchForm, EditProfileDetailsForm, CommentForm
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
    'search_post': template_path+'search_posts.html',
    'edit_comment': template_path+'edit_comment.html',
    'delete_comment': template_path+'delete_comment.html'
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
    admin_user = User.objects.get(id=1)
    form = SearchForm(request.POST)
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search_term = form.cleaned_data['search_term']
            return redirect(reverse('search', kwargs={'search_term': search_term}))
    else:
        pass
    return render(request, template_pages['about'], context={'form': form, 'admin_user': admin_user})


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
    header_image_bool = False
    if post_data.header_image:
        header_image_bool = True

    else:
        header_image_bool = False

    if post_data.likes.filter(id=request.user.id).exists():
        liked = True
    
    form = SearchForm()
    
    if request.method == 'POST' and 'search' in request.POST:
        form = SearchForm(request.POST)
        if form.is_valid():
            search_term = form.cleaned_data['search_term']
            return redirect(reverse('search', kwargs={'search_term': search_term}))

    comment_form = CommentForm(initial={'user_name': request.user, 'post': post_data, "comment": ""})
    if request.method == "POST" and "comments" in request.POST:
        comment_form = CommentForm(request.POST , initial={'user_name': request.user, 'post': post_data, 'comment': "Comment"})
        if comment_form.is_valid():
            print(f"\n {request.user}\n {post_data}")
            data = comment_form.cleaned_data
            new_comment = Comments(user_name=request.user, post=post_data, comment=data['comment'])
            new_comment.save()
            print("What is going on!")
            return redirect(reverse('blogpost', kwargs={'blog_slug': post_data.slug_post}))
        else:
            print(f"\nI am here\n")
            # print(comment_form.user_name, comment_form.post)
    context = {
        "post": post_data,
        "likes": total_likes,
        "liked": liked,
        'post_featured': new_feature_post,
        'form': form,
        'header_image_bool': header_image_bool,
        'comment_form': comment_form,
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
    form = EditProfileDetailsForm()
    
    user_id = User.objects.get(username=request.user)

    if request.method == "POST":
        form = EditProfileDetailsForm(request.POST, request.FILES)
        if form.is_valid():
            update_data = form.cleaned_data
            if len(UserProfile.objects.filter(user=user_id)) > 0:
                user_profile = UserProfile.objects.get(user=user_id)
                print(update_data)
                if update_data['profile_picture']:
                    user_profile.profile_picture = update_data['profile_picture']
                    print(update_data['profile_picture'])
                if update_data['linkedin_link']:
                    user_profile.linkedin_link = update_data['linkedin_link']
                if update_data['github_link']:
                    user_profile.github_link = update_data['github_link']
                if update_data['portfolio_link']:
                    user_profile.portfolio_link = update_data['portfolio_link']
                if update_data['bio']:
                    user_profile.bio = update_data['bio']
                user_profile.save()
                return redirect(reverse_lazy('Home'))
            else:
                print('I am here')
                user_picture = None
                user_linkedin = None
                user_github = None
                user_portfolio = None
                user_bio = None
                if update_data['profile_picture']:
                    user_picture = update_data['profile_picture']
                if update_data['linkedin_link']:
                    user_linkedin = update_data['linkedin_link']
                if update_data['github_link']:
                    user_github = update_data['github_link']
                if update_data['portfolio_link']:
                    user_portfolio = update_data['portfolio_link']
                if update_data['bio']:
                    user_bio = update_data['bio']
                new_profile = UserProfile(user=user_id, profile_picture=user_picture, linkedin_link=user_linkedin, github_link=user_github, portfolio_link=user_portfolio, bio=user_bio)
                new_profile.save()
                return redirect(reverse_lazy('Home'))
    liked_posts = Post.objects.filter(likes=user_id)

    context = {
        'liked_post_all': liked_posts, 
        'form': form,       
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
    fields = ['title', 'slug_post' , 'header_image' , 'blog_meta', 'blog_content', 'topic_tag']
    success_url = reverse_lazy('Home')

class DeletePostView(DeleteView):
    model = Post
    template_name = template_pages['delete_post']
    success_url = reverse_lazy('Home')




def SearchedPostView(request, search_term):
    topic_ids = Topics.objects.filter(topic_tag__contains=search_term)
    topic_post_list = []
    for item in topic_ids:
        topic_post_list.extend(Post.objects.filter(topic_tag=item.id))
    topic_post_list = list(dict.fromkeys(topic_post_list))
    all_posts = Post.objects.all()
    post_data = Post.objects.filter(title__contains=search_term) | Post.objects.filter(blog_content__contains=search_term)
    first_post = all_posts[0]
    most_likes = max([post.total_likes() for post in all_posts])
    most_liked = [post for post in all_posts if post.total_likes() == most_likes]
    most_liked = random.choice(most_liked)
    

    for item in post_data:
        if item in topic_post_list:
            index_item = topic_post_list.index(item)
            topic_post_list.pop(index_item)

    total_found = len(post_data) + len(topic_post_list)
    search_found = False
    if total_found> 0:    
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
        'post_with_topics': topic_post_list
    }
    return render(request, template_pages['search_post'], context=context)

class Registration(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')


class CommentUpdateView(UpdateView):
    form_class = CommentForm
    model = Comments
    template_name = template_pages['edit_comment']
    success_url = reverse_lazy('Home')


class DeleteCommentView(DeleteView):
    form_class = CommentForm
    model = Comments
    template_name = template_pages['delete_comment']
    success_url = reverse_lazy('Home')
