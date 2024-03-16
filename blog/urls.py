from django.urls import path
from . import views

urlpatterns = [
    #FVB
    path('', views.index, name="index"),
    path('login/', views.iniciar_sesion, name="login"),
    path('signup/', views.signup, name="signup"),
    path('logout/', views.cerrar_sesion, name="logout"),
    path('category/<category>/', views.blog_category, name='blog_category'),

    #CVB
    path('BlogPost/<int:pk>/', views.blog_detail, name='blog_detail'),
    path('BlogPost/<int:pk>/edit/', views.BlogPostUpdateView.as_view(), name='edit_post'),
    path('BLogPost/<int:pk>/delete/', views.BlogPostDeleteView.as_view(), name='delete_post'),
    path('new_post/', views.BlogPostCreateView.as_view(), name="new_post"),
    path('about/', views.AboutView.as_view(), name='about'),
    path('contact/', views.ContactView.as_view(), name='contact'),
]