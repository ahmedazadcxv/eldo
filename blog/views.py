from django.contrib.postgres.search import (SearchQuery, SearchRank,
                                            SearchVector)
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.shortcuts import HttpResponseRedirect, get_object_or_404, render
from django.views.generic import ListView

from .forms import NewCommentForm, PostSearchForm
from .models import Category, Comment, Post  


def home(request):

    all_posts = Post.newmanager.all()

    return render(request, 'blog/index.html', {'posts': all_posts, 'Category': Category.objects.all() })


def post_single(request, post):

    post = get_object_or_404(Post, slug=post, status='published')
    postcat = Post.objects.filter(category=post.category)
    
    postcat2 = Category.objects.filter(name=post.category).first().get_family()

    fav = bool

    if post.favourites.filter(id=request.user.id).exists():
        fav = True

    allcomments = post.comments.filter(status=True)
    page = request.GET.get('page', 1)

    paginator = Paginator(allcomments, 10)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    user_comment = None

    if request.method == 'POST':
        comment_form = NewCommentForm(request.POST)
        if comment_form.is_valid():
            user_comment = comment_form.save(commit=False)
            user_comment.post = post
            user_comment.save()
            return HttpResponseRedirect('/' + post.slug)
    else:
        comment_form = NewCommentForm()

    session_key = 'view_post_{}'.format(post)
    if not request.session.get(session_key,False):
        post.views +=1
        post.save()
        request.session[session_key] = True
    return render(request, 'blog/single.html', {'post': post,
    'Category': Category.objects.all(),'Category2': postcat,'Category3': postcat2,
     'comments':  user_comment, 'comments': comments, 'comment_form': comment_form, 'allcomments': allcomments, 'fav': fav})


class CatListView(ListView):
    template_name = 'blog/category.html'
    context_object_name = 'catlist'

    def get_queryset(self):
        content = {
            'cat':  Category.objects.get( slug=self.kwargs['category']),
            'posts': Post.objects.filter(category__slug=self.kwargs['category']).filter(status='published'),
            'Category': Category.objects.all(), 
            'Category11': Category.objects.get( slug=self.kwargs['category']).get_family()
            
        }
        return content


def category_list(request):
    category_list = Category.objects.exclude(name='default')
    context = {
        "category_list": category_list,
    }
    return context


def post_search(request):
    form = PostSearchForm()
    q = ''
    results = []

    if 'q' in request.GET:
        form = PostSearchForm(request.GET)
        if form.is_valid():
            q = form.cleaned_data['q']

            vector = SearchVector('title', weight='A') + \
                SearchVector('content', weight='B')
            query = SearchQuery(q)

            results = Post.objects.annotate(
                rank=SearchRank(vector, query, cover_density=True)).order_by('-rank')

    return render(request, 'blog/search.html',
                  {'form': form,
                   'q': q,
                   'results': results})
