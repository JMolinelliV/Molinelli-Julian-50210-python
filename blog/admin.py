from django.contrib import admin
from blog.models import Category, BlogPost, Comment, Contact, Avatar

# Register your models here.

admin.site.register(Category)
admin.site.register(BlogPost)
admin.site.register(Comment)
admin.site.register(Contact)
admin.site.register(Avatar)
