from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .models import Post, Group, User
from .forms import PostForm

from datetime import datetime


def index(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    title = 'Последние обновления на сайте'
    text = 'Последние обновления на сайте'
    context = {
        'page_obj': page_obj,
        'posts': posts,
        'title': title,
        'text': text
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    posts = User.objects.get(username=username).posts.all()
    post_count =posts.count()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    user_first_name = User.objects.get(username=username).first_name
    user_last_name = User.objects.get(username=username).last_name
    context = {
        'username': username,
        'user_first_name':user_first_name,
        'user_last_name':user_last_name,
        'page_obj': page_obj,
    }
    return render(request, 'posts/profile.html', context)

def post_detail(request, post_id):
    posts = get_object_or_404(Post, pk=post_id)
    title = 'Пост ' + posts.text[:30]
    pub_date = posts.pub_date
    author = posts.author
    posts_count = author.posts.all().count()
    group = posts.group
    context = {
        'posts': posts,
        'title': title,
        'pub_date': pub_date,
        'author': author,
        'posts_count': posts_count,
        'group': group,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.pub_date = datetime.now()
            post.save()
            return redirect('posts:profile', username=request.user)
        else:
            form = PostForm()
    form = PostForm()
    groups = Group.objects.all()
    context = {
        'form': form,
        'groups': groups,
    }
    return render(request, 'posts/create_post.html', context)


@login_required
def post_edit(request, post_id):
    is_edit = True
    post = get_object_or_404(Post, pk=post_id)
    if request.method =='POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.pub_date = datetime.now()
            post.save()
            return redirect('posts:post_detail', post_id=post_id)
        else:
            form = PostForm(instance=post)
    groups = Group.objects.all()
    context = {
        'form': form,
        'groups': groups,
        'is_edit': is_edit,
    }
    return render(request, 'posts/create_post.html', context)
