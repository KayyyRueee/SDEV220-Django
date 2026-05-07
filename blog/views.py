from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from .forms import PostForm
from django.contrib.auth.decorators import login_required      #makes it so only logged in users can create, edit, publish, or delete posts

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
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def post_list(request):
    posts = Post.objects.filter(
        published_date__lte=timezone.now()
    ).order_by('published_date')

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

