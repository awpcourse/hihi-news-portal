# Create your views here.

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from news_portal.forms import UserLoginForm
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, render
from django.db.models import Q
from django.http import HttpResponseRedirect
from urllib import urlencode
from news_portal.models import News, Category, NewsComment
from news_portal.forms import NewsItemCommentForm
from news_portal.forms import SearchForm


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **kwargs):
        view = super(LoginRequiredMixin, cls).as_view(**kwargs)
        return login_required(view)


def index(request):
    form = SearchForm()
    order = ['decreasing', 'increasing']
    criteria = ['title','date-added']
    context = {
        'order': order,
        'criteria': criteria,
        'form': form,
        'categories': Category.objects.all(),
        'posts': News.objects.all()[:5]
    }

    return render(request, 'index.html', context)


def view_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    context = {
        'category': category,
        'posts': News.objects.filter(category=category)
    }
    return render(request, 'view_category.html', context)


@login_required
def news_details(request, slug):
    news_item = News.objects.get(slug=slug)
    category = Category.objects.get(title=news_item.category)
    if request.method == 'GET':
        form = NewsItemCommentForm()
        context = {
            'category': category,
            'post': news_item,
            'form': form,
        }
        return render(request, 'view_post.html', context)
    elif request.method == 'POST':
        form = NewsItemCommentForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            comment = NewsComment(text=text, news_post=news_item, author=request.user)
            comment.save()
        return redirect('news_details', slug=slug)


def login_view(request):
    if request.user.is_authenticated():
        return redirect('index')
    if request.method == 'GET':
        form = UserLoginForm()
        context = {'form': form}
        return render(request, 'login.html', context)
    elif request.method == 'POST':
        form = UserLoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is None:
            context = {
                'form': form,
                'error_message': 'Wrong username or password!'
            }
            return render(request, 'login.html', context)
        else:
            login(request, user)
            return redirect('index')


def logout_view(request):
    logout(request)
    return redirect('index')

@csrf_exempt
def search_view(request):
    if request.method == 'POST':
        if 'q' in request.POST:
            return HttpResponseRedirect("{}?{}".format(
                    request.META['PATH_INFO'], urlencode({'q': request.POST['q']})))

    form = SearchForm(request.GET)
    posts = []
    if form.is_valid():
        q = form.cleaned_data['q']
        posts = News.objects.filter(Q(title__contains=q) | Q(body__contains=q))
    context = {
        'form': form,
        'posts': posts,
    }
    return render(request, 'search.html', context)
