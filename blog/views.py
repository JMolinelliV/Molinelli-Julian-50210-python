from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
from blog.models import Avatar, BlogPost, Comment
from blog.forms import AvatarForm, BlogPostForm, CommentForm, EditUser, UserRegister
from django.db.models import Q
from django.contrib.auth import  login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView

#Imorts para CBV
from django.views.generic import ListView, DeleteView, UpdateView, CreateView, TemplateView, DetailView
from django.urls import reverse, reverse_lazy

# FBV

"""Muestra todos los posteos en index y permite filtrar con la barra de búsqueda dentro de todos los posts"""
def index(request):
    if 'search' in request.GET:
        search = request.GET['search']
        searches = Q(Q(title__icontains=search) | Q(content__icontains=search))
        posts = BlogPost.objects.filter(searches)
    else:
        posts = BlogPost.objects.all().order_by('-creation_date')

    context = {
        "posts":posts,
    }

    return render(request, 'blog/index.html', context)

"""Muestra los posteos por categorias y permite filtrar con la barra de busqueda solo dentro de la categoría"""
def blog_category(request, category):
    if 'search' in request.GET:
        search = request.GET['search']
        searches = Q(Q(title__icontains=search) | Q(content__icontains=search))
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

#CBV 
class BlogPostListView(ListView):
    model = BlogPost
    context_object_name = "posts"
    template_name = 'blog/index.html'

class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post=self.object)
        context['comment_quantity'] = context['comments'].count()
        context['form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.comment_author = request.user
            comment.save()
            return redirect(request.path_info)
        return render(request, self.template_name, self.get_context_data())

class BlogPostCreateView(LoginRequiredMixin, CreateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blog/new_post.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.post_author = self.request.user
        return super().form_valid(form)

class BlogPostUpdateView(LoginRequiredMixin, UpdateView):
    model = BlogPost
    template_name = 'blog/edit_post.html'
    success_url = reverse_lazy('index')
    form_class = BlogPostForm

class BlogPostDeleteView(LoginRequiredMixin, DeleteView):
    model = BlogPost
    template_name = 'blog/delete_post.html'
    success_url = reverse_lazy('index')

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/new_comment.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.comment_author = self.request.user.username
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)

class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    fields = ['content']

    def form_valid(self, form):
        form.save()
        return redirect('blog_detail', pk=self.object.post.pk)

class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment

    def get_success_url(self):
        post_pk = self.object.post.pk
        return reverse('blog_detail', kwargs={'pk': post_pk})

class AboutView(TemplateView):
    template_name = 'blog/about.html'

class ContactView(TemplateView):
    template_name = 'blog/contact.html'
    success_url = reverse_lazy('success_contact')

#Login
def iniciar_sesion(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data = request.POST)

        if form.is_valid():
            info_dic = form.cleaned_data
            user = authenticate(
                username = info_dic["username"],
                password = info_dic["password"]
                )

            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            
        else:
            return HttpResponseRedirect(request.path_info)
    
    else:
        form = AuthenticationForm()

    return render(request, "register/login.html", {"form":form})


#Register
def signup(request):
    if request.method == "POST":
        form = UserRegister(request.POST)

        if form.is_valid():
            form.save()  
            return redirect('index')

    else:
        form = UserRegister()

    return render(request, 'register/signup.html', {"form":form})

#EditUser
@login_required
def user_profile(request, username):
    user = User.objects.get(username=username)
    avatar = Avatar.objects.filter(user=user).first()
    context = {
        'user': user,
        'avatar': avatar,
    }
    return render(request, 'register/user_profile.html', context)

@login_required
def edit_user(request, username):
    
    user = request.user

    if request.method == "POST":
        form = EditUser(request.POST)
        user = user
        if form.is_valid():
            info_dic = form.cleaned_data

            user.email = info_dic["email"]
            user.last_name = info_dic["last_name"]
            user.first_name = info_dic["first_name"]
            user.save()

            return HttpResponseRedirect(reverse("index"))
    
    else:
        form = EditUser(instance=user)

    return render(request, 'register/edit_user.html', {"form":form})

class ChangePassword(LoginRequiredMixin, PasswordChangeView):
    template_name = "register/edit_password.html"
    success_url = reverse_lazy('index')

@login_required
def change_avatar(request, username):
    if request.method == "POST":
        form = AvatarForm(request.POST, request.FILES)

        if form.is_valid():
            info_dic = form.cleaned_data
            user = User.objects.get(username=request.user)
            new_avatar = Avatar(user=user, image=info_dic["image"])
            new_avatar.save()  
            return redirect('index')

    else:
        form = AvatarForm()

    return render(request, 'register/new_avatar.html', {"form":form})

#Logout
@login_required
def cerrar_sesion(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

