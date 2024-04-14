from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse

from .models import Post, Comment
from django.views.generic import ListView

from .forms import CommentForm, AddPostForm
from django.views.decorators.http import require_POST


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    return render(request, 'blog/post/comment.html', {'post': post,
                                                      'form': form,
                                                      'comment': comment})


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 2
    template_name = 'blog/post/list.html'


def post_list(request):
    post_list = Post.published.all()
    paginator = Paginator(post_list, 2)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)
    return render(request, 'blog/post/list.html', {"posts": posts})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day,
                             slug=post)
    comments = post.comments.filter(active=True)
    form = CommentForm()
    return render(request, 'blog/post/detail.html', {"post": post,
                                                     'comments': comments,
                                                     'form': form})


@login_required
def add_post(request):
    if request.method == 'POST':
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.status = form.cleaned_data['status']
            post.image = request.FILES.get('image')
            post.save()
            post.tags.add(*form.cleaned_data['tags'])
            return HttpResponseRedirect(reverse('blog:post_list'))
    else:
        form = AddPostForm()
    return render(request, 'blog/post/add.html', {'form': form})


# Create your views here.
def index(request):
    return HttpResponse('<h1>My first http response</h1>')


def hello(request):
    return HttpResponse("Hello<br>World!!!")
