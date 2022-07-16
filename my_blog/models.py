from django.db import models
from ckeditor.fields import RichTextField
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

class Topics(models.Model):
    topic_tag = models.CharField(null=False, max_length=100)

    def __str__(self):
        return self.topic_tag


class Post(models.Model):
    user_name = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(unique=True, null=False, max_length=65)
    blog_date = models.DateField(auto_now_add=True)
    blog_meta = RichTextField(blank=True, null=True)
    blog_content = RichTextField(blank=True, null=True)
    topic_tag = models.ManyToManyField(Topics, related_name="blog_post")
    slug_post = models.SlugField(null=True, unique=True)
    likes = models.ManyToManyField(User, related_name="blog_post", default=0)

    def total_likes(self):
        return self.likes.count()

    def __str__(self):

        return f"{self.user_name} {self.title} {self.blog_date} {self.blog_meta} {self.blog_content} {self.topic_tag}"
    
    def get_absolute_urls(self):
        return reverse("blogpost", kwargs={"slug_post": self.slug_post})


class Comments(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return '%s - %s' % (self.post.title, self.name)





