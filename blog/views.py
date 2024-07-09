from django.core.paginator import Paginator

from django.shortcuts import render

from blog.models import Post

from django.db.models import Q

PER_PAGE = 9

def index(request):
    posts = Post.objects.get_published() # type: ignore
        

    paginator = Paginator(posts, per_page=PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
        }
    )

def created_by(request, author_id):
    posts = (Post.objects.get_published() # type:ignore
             .filter(created_by__id=author_id)) 
        

    paginator = Paginator(posts, per_page=PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
        }
    )

def category(request, slug):
    posts = (Post.objects.get_published() # type:ignore
             .filter(category__slug=slug)) 
        

    paginator = Paginator(posts, per_page=PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
        }
    )

def tag(request, slug):
    posts = (Post.objects.get_published() # type:ignore
             .filter(tags__slug=slug)) 
        

    paginator = Paginator(posts, per_page=PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
        }
    )

def search(request, slug):
    search_value = 'Qualquer'
    posts = (
            Post.objects.get_published() # type:ignore
                .filter(
                    Q(title__icontains=search_value) |
                    Q(excerpt__icontains=search_value) |
                    Q(content__icontains=search_value)
                )
             ) 
        

    paginator = Paginator(posts, per_page=PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
        }
    )

def page(request, slug): 
    return render(
        request,
        'blog/pages/page.html',
        {
            # 'page_obj': page_obj,
        }
    )


def post(request, slug):
    post = (
        Post.objects.get_published() # type: ignore
        .filter(slug=slug)
        .first()
             ) 
    return render(
        request,
        'blog/pages/post.html',
        {
            'post': post,
        }
    )