from django import forms
from blog.models import BlogPost

class CommentForm(forms.Form):
    comment_author = forms.CharField(
        max_length=60,
        widget=forms.TextInput(
            attrs={"class":"form-control", "placeholder":"Ingresa tu nombre:"}
        ),
    )

    email = forms.EmailField(
        max_length=60,
        widget=forms.TextInput(
            attrs={"class":"form-control", "placeholder": "Email"}
        ),
    )

    content = forms.CharField(
        widget=forms.Textarea(
            attrs={"class":"form-control", "placeholder":"Deja un comentario..."}
        )
    )

#ModelForm creado para darle formatos a BlogPostCreateView y BlogPostUpdateView
class BlogPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BlogPostForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'post_author', 'image', 'categories']

