from django.shortcuts import render

def post_list(request):
    posts = [
        {"title": "First post", "text": "Hello world!"},
        {"title": "Second post", "text": "This is my second post"},
    ]
    return render(request, 'blog/post_list.html', {'posts': posts})