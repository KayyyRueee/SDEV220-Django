from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),   # homepage
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'), #create a new post
    path('drafts/', views.post_draft_list, name='post_draft_list'), #to create a post, but leave it in draft
    path('post/<int:pk>/publish/', views.post_publish, name='post_publish'), #publish a draft
    path('post/<int:pk>/remove/', views.post_remove, name='post_remove'), #delete
]