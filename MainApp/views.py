from typing import Union

from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.db.models import Count
from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from MainApp.models import Snippet, Comment
from MainApp.forms import SnippetForm, UserRegistrationForm, CommentForm


def index_page(request):
    snippet_id = request.GET.get("id")
    if snippet_id:
        try:
            snippet = Snippet.objects.get(pk=snippet_id)
            comment_form = CommentForm()
            context = {'pagename': 'Страница сниппета',
                       'snippet': snippet,
                       'comment_form': comment_form,
                       }
            return render(request, 'pages/snippet_detail.html', context)
        except:
            return render(request, 'pages/error_search.html')
    else:
        context = {'pagename': 'PythonBin'}
        return render(request, 'pages/index.html', context)


@login_required
def add_snippet_page(request):
    if request.method == "GET":   #пользователю нужна страница с формой
        form = SnippetForm()
        context = {'pagename': 'Добавление нового сниппета', 'form': form}
        return render(request, 'pages/add_snippet.html', context)
    if request.method == "POST":   # получение данных от формы
        form = SnippetForm(request.POST)
        if form.is_valid():
            snippet = form.save(commit=False)
            snippet.user = request.user
            snippet.save()
            return redirect("snippet-list")

def snippets_page(request):
    lang = request.GET.get("lang")
    sort = request.GET.get('sort')
    user_sort = request.GET.get('user')
    all_users = User.objects.all()
    all_id = []
    for user in all_users:
        all_id.append(user.id)
    user_with_one_id = []
    for char in all_id:
        if Snippet.objects.filter(user_id=char).count() >= 1:
            user_with_one_id.append(char)
    users_with_one_snippet = User.objects.filter(pk__in = user_with_one_id)
    try:
        mine = Snippet.objects.filter(user=request.user)
    except TypeError:
        mine = None
    public = Snippet.objects.filter(privacy=False)
    if mine:
        mine_public = mine | public
    else:
        mine_public = public
    if lang:
        mine_public = mine_public.filter(lang=lang)
    if sort:
        mine_public = mine_public.order_by(sort)
    if user_sort:
        chosen_id = User.objects.get(username=user_sort)
        mine_public = mine_public.filter(user_id=chosen_id)
    count = Snippet.objects.count()
    context = {'pagename': 'Просмотр сниппетов',
               'count': count,
               'mine_public': mine_public,
               'sort': sort,
               'lang': lang,
               'users_with_one_snippet': users_with_one_snippet,
               'user_sort': user_sort
               }
    return render(request, 'pages/view_snippets.html', context)


@login_required
def snippets_my_snippets(request):
    lang = request.GET.get("lang")
    sort = request.GET.get('sort')
    my_snippets = Snippet.objects.filter(user=request.user)
    count = Snippet.objects.filter(user=request.user).count()
    if lang:
        my_snippets = my_snippets.filter(lang=lang)
    if sort:
        my_snippets = my_snippets.order_by(sort)
    context = {'pagename': 'Мои сниппеты',
               'my_snippets': my_snippets,
               'count': count,
               'sort': sort,
               'lang': lang
               }
    return render(request, 'pages/my_snippets.html', context)


@login_required()
def snippet_delete(request, snippet_id):
    snippet = Snippet.objects.get(pk=snippet_id)
    snippet.delete()
    return redirect("snippet-list")


@login_required()
def snippet_change(request, snippet_id):
    snippet = Snippet.objects.get(pk=snippet_id)
    if request.method == "GET":   #пользователю нужна страница с формой
        form = SnippetForm(initial={'name': snippet.name, 'lang': snippet.lang, 'code': snippet.code,
        'privacy': snippet.privacy})
        context = {'pagename': 'Изменение сниппета №', 'form': form,'snippet':snippet}
        return render(request, 'pages/change_snippet.html', context)
    if request.method == "POST":   # получение данных от формы
        form = SnippetForm(request.POST)
        if form.is_valid():
            snippet.delete()
            snippet = form.save(commit=False)
            snippet.user = request.user
            snippet.pk = snippet_id
            snippet.save()
            return redirect("snippet-list")


def snippet_detail(request, snippet_id):
    snippet = Snippet.objects.get(pk=snippet_id)
    user = request.user.username
    voted = snippet.voted
    comment_form = CommentForm()
    context = {'pagename': 'Страница сниппета',
               'snippet': snippet,
               'comment_form': comment_form,
               'user': user,
               'voted': voted
               }
    return render(request, 'pages/snippet_detail.html', context)


def login_page(request):
   if request.method == 'POST':
       username = request.POST.get("username")
       password = request.POST.get("password")
       # print("username =", username)
       # print("password =", password)
       user = auth.authenticate(request, username=username, password=password)
       if user is not None:
           auth.login(request, user)
       else:
           # Return error message
           pass
   return redirect(request.META.get('HTTP_REFERER', '/'))


def logout(request):
    auth.logout(request)
    return redirect('home')


def create_user(request):
    if request.method == "GET":   #пользователю нужна страница с формой
        form = UserRegistrationForm()
        context = {'pagename': 'Регистрация', 'form': form}
        return render(request, 'pages/create_user.html', context)
    if request.method == "POST":   # получение данных от формы
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')


@login_required()
def add_comment(request):
    if request.method == "POST":
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            snippet_id = request.POST['snippet_id']
            snippet = Snippet.objects.get(pk=snippet_id)
            comment = form.save(commit=False)
            comment.author = request.user
            comment.snippet = snippet
            comment.save()
            return redirect(request.META.get('HTTP_REFERER', '/'))


def user_page(request, snippet_user):
    lang = request.GET.get("lang")
    sort = request.GET.get('sort')
    chosen_user = snippet_user
    user_object = User.objects.get(username=chosen_user)
    user_id = user_object.id
    snippets = Snippet.objects.filter(user_id=user_id).filter(privacy=False)
    if lang:
        snippets = snippets.filter(lang=lang)
    if sort:
        snippets = snippets.order_by(sort)
    count = Snippet.objects.filter(user_id=user_id).filter(privacy=False).count()
    context = {'chosen_user': chosen_user,
               'snippets': snippets,
               'sort': sort,
               'lang': lang,
               'count': count
               }
    return render(request, 'pages/user_page.html', context)


def users_rating(request):
    sort = request.GET.get('sort')
    users = User.objects.annotate(num_snippets=Count('snippet')).annotate(num_comments=Count('comment')).order_by('-num_snippets')
    count_snippets = Snippet.objects.all().count()
    count_comments = Comment.objects.all().count()
    if sort:
        users = users.order_by(sort)
    context = {'users': users,
               'count_snippets': count_snippets,
               'count_comments': count_comments,
               'sort': sort
               }
    return render(request, 'pages/users_rating.html', context)

@login_required()
def snippet_thumbs_up(request, snippet_id):
    user = request.user.username
    snippet = Snippet.objects.get(pk=snippet_id)
    snippet.rating += 1
    snippet.voted += user
    snippet.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required()
def snippet_thumbs_down(request, snippet_id):
    user = request.user.username
    snippet = Snippet.objects.get(pk=snippet_id)
    snippet.rating -= 1
    snippet.voted += user
    snippet.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))

