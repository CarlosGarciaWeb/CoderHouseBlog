from . import views
from django.urls import path

urlpatterns = [
    path('', views.Home, name='Home'),
    path('about/', views.About, name='about'),
    path('blog/<slug:blog_slug>/', views.BlogPost, name='blogpost'),
    path('like/<int:pk>', views.Like, name='like'),
    path('add-post/', views.AddPostView.as_view(), name='add_post'),
    path('users/<user>/', views.User, name='users'),
    path('edit_profile/<user>/', views.UserEditView.as_view(), name='edit_profile'),
    path('register/', views.Registration.as_view(template_name='my_blog/register.html'), name='register'),
    path('login/', views.Registration.as_view(template_name='registration/login.html'), name='login'),
    path('edit-post/<slug:pk>', views.UpdatePostView.as_view(), name='update'),
]
