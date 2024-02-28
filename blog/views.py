from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from blog.models import BlogPost, Comment
from blog.forms import CommentForm, newPostForm
from django.db.models import Q

# Create your views here.

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

"""Muestra los comentarios de un BLogPost buscando por la PrimaryKey"""
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

def new_post(request):
    if request.method == "POST":
        form = newPostForm(request.POST)
        if form.is_valid():
            instance = form.save()
            instance.post_author = request.user
            instance.save()
            return redirect("index")
        
    else:
        form = newPostForm()
    
    context = {
        "form":newPostForm()
    }

    return render(request, "blog/new_post.html", context)