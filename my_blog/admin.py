from django.contrib import admin
from .models import Post, Topics, Comments, UserProfile
# Register your models here.

admin.site.register([Post, Topics, Comments, UserProfile])