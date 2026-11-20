from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import never_cache

from .models import Post

# Create your views here.


@never_cache
def render_posts(request):

    posts = Post.objects.order_by("-date")

    return render(request, 'posts.html', {'posts': posts})


@never_cache
def post_detail(request, post_id):

    post = get_object_or_404(Post, pk=post_id)

    return render(request, 'post_detail.html', {'post': post})
