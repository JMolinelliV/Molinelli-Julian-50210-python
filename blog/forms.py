from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from blog.models import Category

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

class newPostForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('enviar', 'Enviar'))

    CATEGORIES = (
        (1, "Agua dulce"),
        (2, "Agua marina"),
        (3, "Primer acuario"),
        (4, "Alimentación")
    )

    título = forms.CharField(max_length=250)
    contenido = forms.CharField(
        widget=forms.Textarea()
    )
    imagen = forms.ImageField()
    autor = forms.CharField()
    categorias = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )