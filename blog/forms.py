from django import forms
from blog.models import BlogPost, Comment
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['content'].widget.attrs['class'] = 'form-control'
        self.fields['content'].widget.attrs['placeholder'] = 'Escribe tu comentario...'

#ModelForm creado para darle formatos a BlogPostCreateView y BlogPostUpdateView
class BlogPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BlogPostForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'image', 'categories']

class UserRegister(UserCreationForm):

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "password1", "password2"]

class EditUser(UserChangeForm):

    password = None

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]

class AvatarForm(forms.Form):
    image = forms.ImageField()