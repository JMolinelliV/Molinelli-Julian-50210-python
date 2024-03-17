from django.urls import path
from . import views

urlpatterns = [
    #FVB
    path('', views.index, name="index"),
    path('login/', views.iniciar_sesion, name="login"),
    path('signup/', views.signup, name="signup"),
    path('logout/', views.cerrar_sesion, name="logout"),
    path('edit_user/<str:username>/', views.edit_user, name="edit_user"),
    path('category/<category>/', views.blog_category, name='blog_category'),
    path('new_avatar/<str:username>/', views.change_avatar, name="new_avatar"),

    #CVB
    path('BlogPost/<int:pk>/', views.BlogPostDetailView.as_view(), name='blog_detail'),
    path('BlogPost/<int:pk>/edit/', views.BlogPostUpdateView.as_view(), name='edit_post'),
    path('BLogPost/<int:pk>/delete/', views.BlogPostDeleteView.as_view(), name='delete_post'),
    path('new_post/', views.BlogPostCreateView.as_view(), name="new_post"),
    path('about/', views.AboutView.as_view(), name='about'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('comment/<int:pk>/edit/', views.CommentUpdateView.as_view(), name='edit_comment'),
    path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='delete_comment'),
    path("change_password/<str:username>/", views.ChangePassword.as_view(), name="change_password"),
]