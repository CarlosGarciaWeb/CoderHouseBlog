from . import views
from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.Home, name='Home'),
    path('about/', views.About, name='about'),
    path('blog/<slug:blog_slug>/', views.BlogPost, name='blogpost'),
    path('like/<int:pk>', views.Like, name='like'),
    path('add-post/', views.AddPostView.as_view(), name='add_post'),
    path('users/<user_name>/', views.UserView, name='users'),
    path('edit-profile/', views.UserEditView.as_view(), name='edit_profile'),
    path ('password/', auth_views.PasswordChangeView.as_view(template_name='registration/change_password.html', success_url = reverse_lazy('login'))),
    path('register/', views.Registration.as_view(template_name='my_blog/register.html'), name='register'),
    path('login/', views.Registration.as_view(template_name='registration/login.html'), name='login'),
    path('edit-post/<slug:pk>', views.UpdatePostView.as_view(), name='update'),
    path('delete-post/<slug:pk>', views.DeletePostView.as_view(), name='delete'),
    path('search/<str:search_term>', views.SearchedPostView, name='search')
]
