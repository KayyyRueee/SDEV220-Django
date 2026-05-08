from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required      #makes it so only logged in users can create, edit, publish, or delete posts
from django.http import HttpResponseForbidden

from django.shortcuts import render, get_object_or_404, redirect

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()

    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    edit_id = request.GET.get("edit")
    form = None

    if edit_id:
        comment = get_object_or_404(Comment, pk=edit_id)
        form = CommentForm(instance=comment)

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'form': form,
        'comment_edit_id': int(edit_id) if edit_id else None
    })

@login_required
def post_list(request):
    posts = Post.objects.filter(
        published_date__isnull=False
        ).order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

@login_required
def post_draft_list(request):
    posts = Post.objects.filter(
        published_date__isnull=True
    ).order_by('created_date')

    return render(
        request,
        'blog/post_draft_list.html',
        {'posts': posts}
    )

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if post.author != request.user:
        return HttpResponseForbidden("You cannot edit this post.")

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)

    else:
        form = PostForm(instance=post)

    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')


from django.contrib.auth import login
from .forms import RegisterForm

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = RegisterForm()

    return render(request, "registration/register.html", {"form": form})

from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    return render(request, "registration/profile.html")

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

VALID_COMPANY_CODES = ["CompA1", "CompB2", "CompC3"]

def register(request):
    error = None

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        code = request.POST.get("company_code")

        # check company code FIRST
        if code not in VALID_COMPANY_CODES:
            error = "Invalid company code. You are not authorized to register."
        elif form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()

    return render(request, "registration/register.html", {
        "form": form,
        "error": error
    })

@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()

    return render(request, 'blog/add_comment_to_post.html', {'form': form})

@login_required
def comment_edit(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    # only comment author can edit
    if comment.author != request.user.username:
        return redirect('post_detail', pk=comment.post.pk)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=comment.post.pk)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'blog/comment_edit.html', {'form': form})

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    # allow comment author OR post author
    if comment.author != request.user.username and comment.post.author != request.user:
        return redirect('post_list')

    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)


