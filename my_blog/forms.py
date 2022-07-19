from tkinter import Widget
from turtle import width
from django import forms
from .models import Post, UserProfile, Comments
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox

class SignUpForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'captcha')
    

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'


class PostForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

    class Meta:
        model = Post
        fields = ('title', 'slug_post' , 'header_image' ,'topic_tag', 'blog_meta', 'blog_content', 'captcha' )
        
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'topic_tag': forms.SelectMultiple(attrs={'class': 'form-check', 'type': 'checkbox'}),
            'blog_meta': forms.Textarea(attrs={'class': 'form-control'}),
            'blog_content': forms.Textarea(attrs={'class': 'form-control'}),
        }

class EditProfileDetailsForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)
    
    class Meta:
        model = UserProfile
        fields = ('profile_picture', 'linkedin_link', 'github_link', 'portfolio_link', 'bio')
        widgets = {
            'linkedin_link': forms.URLInput(attrs={'class': 'form-control'}),
            'github_link': forms.URLInput(attrs={'class': 'form-control'}),
            'portfolio_link': forms.URLInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control'}),
        }


# class CommentForm(forms.ModelForm):
#     captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

#     class Meta:
#         model = Comments


class ProfileChangeForm(UserChangeForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'captcha')


    

    def __init__(self, *args, **kwargs):
        super(ProfileChangeForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'


class SearchForm(forms.Form):
    search_term = forms.CharField(label='', required=False, max_length=50, widget=forms.TextInput(attrs={'class': 'form-control-sm w-75', 'placeholder': 'Search', 'required': 'True'}))

