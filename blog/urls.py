from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('BlogPost/<int:pk>/', views.blog_detail, name='blog_detail'),
    path('category/<category>/', views.blog_category, name='blog_category'),
    path('new_post/', views.new_post, name="new_post"),
]