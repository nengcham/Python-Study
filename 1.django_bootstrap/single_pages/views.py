from django.shortcuts import render
from blog.models import Post


def landing(request):
    recent_post = Post.objects.order_by('-pk')[:3]
    return render(
        request,
        'single_pages/landing.html',
        {
            'recent_post': recent_post,
        }
    )


def about_me(request):
    return render(
        request,
        'single_pages/about_me.html'
    )
