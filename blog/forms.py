from django import forms

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
        ),
    )

class newPostForm(forms.Form):
    title = forms.CharField(
        widget=forms.TextInput(
            attrs={"class":"form-control", "placeholder":"Título del post"}
        ),
    )

    post_author = forms.CharField(
        widget=forms.TextInput(
            attrs={"class":"form-control", "placeholder":"¿Cómo quieres que te conozcan?"}
        )
    )

    image = forms.ImageField(
        widget=forms.ImageField(
            required=True
        )
    )

    # categories = forms.

    """title = models.CharField(max_length=250)
        content = models.TextField()  #usar RichTextFIeld cuando pueda resolver el import
        post_author = models.ForeignKey(User, on_delete=models.CASCADE) #Si se borra el User todos los BlogPost dependientes se borran
        creation_date = models.DateTimeField(auto_now_add=True)
        modification_date = models.DateTimeField(auto_now=True)
        image = models.ImageField(upload_to='blog/files/blog_images')
        categories = models.ManyToManyField('Category', related_name='posts')"""