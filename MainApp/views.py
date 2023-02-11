from typing import Union

from django.contrib.auth import login, authenticate
from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from MainApp.models import Snippet, Comment
from MainApp.forms import SnippetForm, UserRegistrationForm, CommentForm


def index_page(request):
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
    # snippets = Snippet.objects.all()
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
    count = Snippet.objects.count()
    context = {'pagename': 'Просмотр сниппетов',
               'public': public,
               'count': count,
               'mine_public': mine_public,
               'sort': sort
               }
    return render(request, 'pages/view_snippets.html', context)


@login_required
def snippets_my_snippets(request):
    my_snippets = Snippet.objects.filter(user=request.user)
    count = len(my_snippets)
    context = {'pagename': 'Мои сниппеты',
               'my_snippets': my_snippets,
               'count': count
               }
    return render(request, 'pages/my_snippets.html', context)


@login_required()
def snippet_delete(request, snippet_id):
    snippet = Snippet.objects.get(pk=snippet_id)
    snippet.delete()
    return redirect(request.META.get('HTTP_REFERER', '/'))


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
    comment_form = CommentForm()
    context = {'pagename': 'Страница сниппета',
               'snippet': snippet,
               'comment_form': comment_form,
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
        form = CommentForm(request.POST)
        if form.is_valid():
            snippet_id = request.POST['snippet_id']
            snippet = Snippet.objects.get(pk=snippet_id)
            comment = form.save(commit=False)
            comment.author = request.user
            comment.snippet = snippet
            comment.save()
            return redirect(request.META.get('HTTP_REFERER', '/'))

