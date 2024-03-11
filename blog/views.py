from django.shortcuts import render
from django.http import HttpResponseRedirect
from blog.models import BlogPost, Comment
from blog.forms import BlogPostForm, CommentForm
from django.db.models import Q
from django.contrib.auth import  login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


#Imorts para CBV
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView, TemplateView, FormView
from django.urls import reverse_lazy

# FBV

"""Muestra todos los posteos en index y permite filtrar con la barra de búsqueda dentro de todos los posts"""
def index(request):
    if 'q' in request.GET:
        q = request.GET['q']
        searches = Q(Q(title__icontains=q) | Q(content__icontains=q))
        posts = BlogPost.objects.filter(searches)
    else:
        posts = BlogPost.objects.all().order_by('-creation_date')

    context = {
        "posts":posts,
    }

    return render(request, 'blog/index.html', context)


"""Muestra los posteos por categorias y permite filtrar con la barra de busqueda solo dentro de la categoría"""
def blog_category(request, category):
    if 'q' in request.GET:
        q = request.GET['q']
        searches = Q(Q(title__icontains=q) | Q(content__icontains=q))
        posts = BlogPost.objects.filter(
        categories__cat_name__contains=category
    ).order_by("-creation_date").filter(searches)

    else:
        posts = BlogPost.objects.filter(
            categories__cat_name__contains=category
        ).order_by("-creation_date")

    context = {
        "category": category,
        "posts": posts,
    }
    return render(request, "blog/category.html", context)

"""Muestra solo un post y los comentarios relacionados con la pk de ese post"""
def blog_detail(request, pk):
    
    post = BlogPost.objects.get(pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(
                comment_author = form.cleaned_data["comment_author"],
                email = form.cleaned_data["email"],
                content = form.cleaned_data["content"],
                post=post,
            )
            comment.save()
            return HttpResponseRedirect(request.path_info)
        
    comments = Comment.objects.filter(post=post)
    comment_quantity = len(comments)
    context = {
        "post":post,
        "comments":comments,
        "comment_quantity":comment_quantity,
        "form": CommentForm(),
    }

    return render(request, 'blog/detail.html', context)


#CBV 

class BlogPostListView(ListView):
    model = BlogPost
    context_object_name = "posts"
    template_name = 'blog/index.html'

class BlogPostCreateView(CreateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blog/new_post.html'
    success_url = '/'
    labels = {'title':'título'}

    def form_valid(self, form):
        return super().form_valid(form)

class BlogPostUpdateView(UpdateView): #TODO: no funciona
    model = BlogPost
    template_name = 'blog/edit_post.html'
    success_url = reverse_lazy('index')
    form_class = BlogPostForm

class BlogPostDeleteView(DeleteView):
    model = BlogPost
    template_name = 'blog/delete_post.html'
    success_url = reverse_lazy('index')

class AboutView(TemplateView):
    template_name = 'blog/about.html'

class ContactView(TemplateView):
    template_name = 'blog/contact.html'
    success_url = reverse_lazy('success_contact')

#Log

def login_request(request):

    if request.method == "POST":
        form = AuthenticationForm(request, data = request.POST)

        if form.is_valid():
            user = form.cleaned_data.get('username')
            password = form.changed_data.get('password')

            user = authenticate(username=user, password=password)

            if user is not None:
                login(request, user)

                return render(request, 'blog/index.html', {"mensaje":f"Bienvenido {user}"})
            else:
                return render(request, 'blog/index.html', {"mensaje":"Datos incorrectos!"})
            
        else:
            return render(request, 'blog/index.html', {"mensaje":"Usuario o contraseña incorrectos!"})
        
    form = AuthenticationForm()

    return render(request, 'blog/login.html', {'form':form})

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = 'blog/register.html'