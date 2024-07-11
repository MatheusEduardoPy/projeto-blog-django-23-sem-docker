from django.core.paginator import Paginator

from django.shortcuts import render

from blog.models import Post, Page

from django.db.models import Q

from django.contrib.auth.models import User

from django.http import Http404

from django.views.generic import ListView


PER_PAGE = 9

class PostListView(ListView):
    template_name = 'blog/pages/index.html'
    context_object_name = 'posts'
    paginate_by = PER_PAGE
    queryset = Post.objects.get_published() # type: ignore

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'page_title': 'Home - ',
        })

        return context

def created_by(request, author_id):
    user = User.objects.filter(pk=author_id).first()

    if user is None:
        raise Http404("O usuário não existe")

    posts = (Post.objects.get_published() # type:ignore
             .filter(created_by__id=author_id)) 
    user_full_name = user.username

    if user.first_name:
        user_full_name = f'{user.first_name} {user.last_name}'
    page_title = 'Posts de ' + user_full_name + ' - '

    paginator = Paginator(posts, per_page=PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            'page_title': page_title,
        }
    )

class CreatedByListView(PostListView):
    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs) 

        print('ARGUMENTOS', self.kwargs)

        author_id = 1
        user = User.objects.filter(pk=author_id).first()

        if user is None:
            raise Http404("O usuário não existe")

        user_full_name = user.username

        if user.first_name:
            user_full_name = f'{user.first_name} {user.last_name}'
        page_title = 'Posts de ' + user_full_name + ' - '

        context.update({
            'page_title': page_title
        })

        return context

def category(request, slug):
    posts = (Post.objects.get_published() # type:ignore
             .filter(category__slug=slug)) 
        
    paginator = Paginator(posts, per_page=PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    if len(page_obj) == 0:
        raise Http404() 
    
    page_title = f'{page_obj[0].category.name} - Categoria - '

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            'page_title': page_title,
        }
    )

def tag(request, slug):
    posts = (Post.objects.get_published() # type:ignore
             .filter(tags__slug=slug)) 
        

    paginator = Paginator(posts, per_page=PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    if len(page_obj) == 0:
        raise Http404() 
    
    page_title = f'{page_obj[0].tags.first().name} - Tag - '

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            'page_title': page_title,
        }
    )

def search(request):
    search_value = request.GET.get('search','').strip()
    posts = (   
            Post.objects.get_published() # type:ignore
                .filter(
                    Q(title__icontains=search_value) |
                    Q(excerpt__icontains=search_value) |
                    Q(content__icontains=search_value)
                )[:PER_PAGE]
             ) 
    
    if page is None:
        raise Http404()

    page_title = f'{search_value[:30]} - Search - '

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': posts,
            'search_value': search_value,
            'page_title': page_title,
        }
    )

def page(request, slug): 
    page_obj = (
    Page.objects.filter(is_published=True) # type: ignore
        .filter(slug=slug)
        .first()
             ) 
    
    if page_obj is None:
        raise Http404()

    page_title = f'{page_obj.title} - Página - '

    return render( 
        request,
        'blog/pages/page.html',
        { 
            'page': page_obj,
            'page_title': page_title, 
        }
    )   


def post(request, slug):
    post_obj = (
        Post.objects.get_published() # type: ignore
        .filter(slug=slug)
        .first()
             ) 
    
    if post_obj is None:
        raise Http404()

    page_title = f'{post_obj.title} - Post - '

    return render(
        request,
        'blog/pages/post.html',
        {
            'post': post_obj,
            'page_title': page_title,
        }
    )