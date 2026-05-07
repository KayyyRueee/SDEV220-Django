from django.urls import path
from . import views
from blog import views as blog_views

urlpatterns = [
    path('', views.post_list, name='post_list'),   # homepage
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'), #create a new post
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('drafts/', views.post_draft_list, name='post_draft_list'), #to create a post, but leave it in draft
    path('post/<int:pk>/publish/', views.post_publish, name='post_publish'), #publish a draft
    path('post/<int:pk>/remove/', views.post_remove, name='post_remove'), #delete
    path('accounts/profile/', views.profile, name='profile'), #profiles
    path('accounts/register/', blog_views.register, name='register'), #register to make an account
    path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'), #add a comment to post
]