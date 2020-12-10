from django.shortcuts import render, get_object_or_404, redirect
from .models import Author, Article, Category, Comment
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from .forms import CreateForm, CrateAuthor, CommentForm, CategoryForm, CommentFormAgain
from django.contrib import messages
from django.http import HttpResponseRedirect


def home(request):
    if request.user.is_authenticated:
        user = get_object_or_404(User, id=request.user.id)
        get_author = Author.objects.filter(name=user.id)
        if get_author:
            auth = get_object_or_404(Author, name=user.id)
        else:
            form = CrateAuthor(request.POST or None, request.FILES or None)
            cat = Category.objects.all()
            if request.method == "POST":
                form = CrateAuthor(request.POST or None, request.FILES or None)
                if form.is_valid():
                    instance = form.save(commit=False)
                    instance.name = user
                    instance.save()
                    return redirect('index')
            return render(request, "blog/create_author.html", {"form": form, "cat": cat})

    else:
        auth = None

    post = Article.objects.all().order_by('-posted_on')
    search = request.GET.get('index_search')
    if search:
        post = post.filter(
            Q(title__icontains=search) | Q(body__icontains=search)
        )

    paginator = Paginator(post, 8)  # Show 25 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    cat = Category.objects.all()

    context = {
        "auth": auth,
        "post": page_obj,
        "cat": cat,
    }
    return render(request, 'blog/index.html', context)


def getsingle(request, id):
    if request.user.is_authenticated:
        get_author = get_object_or_404(User, username=request.user.username)
        auth = get_object_or_404(Author, name=get_author.id)
    else:
        auth = None
    post = get_object_or_404(Article, pk=id)
    first = Article.objects.first()
    last = Article.objects.last()
    related = Article.objects.filter(category=post.category).exclude(id=id)[:3]
    getComment = Comment.objects.filter(post=id)
    cat = Category.objects.all()

    if request.user.is_authenticated:
        form = CommentFormAgain(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.post = post
            instance.name = auth.name
            instance.email = auth.email
            instance.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form = CommentForm(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.post = post
            instance.save()
            return HttpResponseRedirect(request.path_info)

    context = {
        "post": post,
        "first": first,
        "last": last,
        "related": related,
        "auth": auth,
        "form": form,
        "comment": getComment,
        "cat": cat,
    }
    return render(request, 'blog/single.html', context)


def getcategory(request, name):
    cat = get_object_or_404(Category, name=name)
    post = Article.objects.filter(category=cat.id)
    cate = Category.objects.all()

    if request.user.is_authenticated:
        get_author = get_object_or_404(User, username=request.user.username)
        auth = get_object_or_404(Author, name=get_author.id)
    else:
        auth = None

    context = {
        "post": post,
        "cat": cat,
        "cate": cate,
        "auth": auth,
    }
    return render(request, 'blog/category.html', context)


def getauthor(request, name):
    get_author = get_object_or_404(User, username=name)
    author = get_object_or_404(Author, name=get_author.id)
    post = Article.objects.filter(author_name=author.id).order_by('-posted_on')
    cat = Category.objects.all()

    if request.user.is_authenticated:
        get_author = get_object_or_404(User, username=request.user.username)
        auth = get_object_or_404(Author, name=get_author.id)
    else:
        auth = None

    context = {
        "author": author,
        "post": post,
        "cat": cat,
        "auth": auth,
    }
    return render(request, 'blog/profile.html', context)


def create_post(request):
    if request.user.is_authenticated:
        get_author = get_object_or_404(User, username=request.user.username)
        auth = get_object_or_404(Author, name=get_author.id)
        get_user = get_object_or_404(Author, name=request.user.id)
        form = CreateForm(request.POST or None, request.FILES or None)
        cat = Category.objects.all()
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author_name = get_user
            instance.save()
            return redirect('index')
        context = {
            "form": form,
            "auth": auth,
            "cat": cat,
        }

        return render(request, 'blog/create.html', context)
    else:
        return redirect('login')


def get_all_blogs(request):
    if request.user.is_authenticated:
        author_user = get_object_or_404(Author, name=request.user.id)
        post = Article.objects.filter(author_name=author_user.id)

        get_author = get_object_or_404(User, username=request.user.username)
        auth = get_object_or_404(Author, name=get_author.id)

        cat = Category.objects.all()

        context = {
            "auth": auth,
            "post": post,
            "cat": cat,
        }

        return render(request, 'blog/all_blogs.html', context)

    else:
        return redirect('login')


def update_post(request, pid):
    if request.user.is_authenticated:
        get_user = get_object_or_404(Author, name=request.user.id)
        post = get_object_or_404(Article, id=pid)
        form = CreateForm(request.POST or None, request.FILES or None, instance=post)
        get_author = get_object_or_404(User, username=request.user.username)
        auth = get_object_or_404(Author, name=get_author.id)
        cat = Category.objects.all()
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author_name = get_user
            instance.save()
            return redirect('all_blogs')
        return render(request, 'blog/create.html', {"form": form, "auth": auth, "cat": cat})
    else:
        return redirect('login')


def delete_post(request, pid):
    if request.user.is_authenticated:
        post = get_object_or_404(Article, id=pid)
        post.delete()
        return redirect('all_blogs')

    else:
        return redirect('login')


def update_profile(request, name):
    if request.user.is_authenticated:
        user = get_object_or_404(User, id=request.user.id)
        get_author = get_object_or_404(User, username=name)
        author = get_object_or_404(Author, name=get_author.id)
        form = CrateAuthor(request.POST or None, request.FILES or None, instance=author)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.name = user
            instance.save()
            return redirect('index')
        return render(request, "blog/create_author.html", {"form": form})
    else:
        return redirect('login')








#
# def getTopic(request):
#     if request.user.is_authenticated:
#         # if request.user.is_staff or request.user.is_superuser:
#         # else: raise Http404('message')
#         get_author = get_object_or_404(User, username=request.user.username)
#         auth = get_object_or_404(Author, name=get_author.id)
#         query = Category.objects.all().order_by('-id')
#         form = CategoryForm(request.POST or None)
#         if form.is_valid():
#             instance = form.save(commit=False)
#             instance.save()
#             messages.success(request, 'Category i'
#                                       's Created! ')
#             return redirect('topics')
#
#         context = {
#             "query": query,
#             "form": form,
#             "auth": auth,
#         }
#         return render(request, 'blog/topics.html', context)
#     else:
#         return redirect('login')
#


#
# def delete_topics(request, id):
#     if request.user.is_authenticated:
#         post = get_object_or_404(Category, id=id)
#         post.delete()
#         return redirect('topics')
#
#     else:
#         return redirect('topics')
#
#
# def update_topics(request):
#
