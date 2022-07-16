from django import forms
from .models import Post
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))

    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'topic_tag', 'slug_post', 'blog_meta', 'blog_content')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'topic_tag': forms.SelectMultiple(attrs={'class': 'form-check', 'type': 'checkbox'}),
            'blog_meta': forms.Textarea(attrs={'class': 'form-control'}),
            'blog_content': forms.Textarea(attrs={'class': 'form-control'}),
        }