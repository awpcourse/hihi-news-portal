# Create your views here.

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from forms import MyRegistrationForm
from django.shortcuts import render_to_response, get_object_or_404
from news_portal.forms import UserLoginForm
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, render
from django.db.models import Q
from django.db.models import F
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from urllib import urlencode
from news_portal.models import News, Category, NewsComment
from news_portal.forms import NewsItemCommentForm
from news_portal.forms import SearchForm


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **kwargs):
        view = super(LoginRequiredMixin, cls).as_view(**kwargs)
        return login_required(view)



def page_hit_decorator(fun):
    def fake_view(request, *args, **kwargs):
        response = fun(request, *args, **kwargs)
        print (' i can haz decorator')
        return response
    return fake_view

def index(request):
    search_form = SearchForm()
    context = {
        'search_form': search_form,
        'categories': Category.objects.all(),
        'posts': News.objects.all()[:5]
    }
    return render(request, 'index.html', context)

def view_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    search_form = SearchForm()
    all_posts = News.objects.filter(category=category)
    paginator = Paginator(all_posts, 2)
    page = request.GET.get('page', 1)
    posts = paginator.page(page)
    context = {
        'search_form': search_form,
        'category': category,
        'categories': Category.objects.all(),
        'posts': posts,
    }
    return render(request, 'view_category.html', context)

@page_hit_decorator
def news_details(request, slug):
    news_item = News.objects.get(slug=slug)
    news_item.increase_count_hit()
    news_item.save()
    news_item.count_hit = F('count_hit') + 1
    news_item.save()
    category = news_item.category
    search_form = SearchForm()
    if request.method == 'GET':
        form = NewsItemCommentForm()
        context = {
            'search_form': search_form,
            'category': category,
            'categories': Category.objects.all(),
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

def register_user(request):
    if request.user.is_authenticated():
        return redirect('index')
    form = None
    if request.method == 'GET':
        form = MyRegistrationForm()
    elif request.method == 'POST':
        form = MyRegistrationForm(request.POST)  # create form object
        if form.is_valid():
            form.save()
            return redirect('index')
    args = {}
    args.update(csrf(request))
    args['form'] = form
    print args
    return render(request, 'register_user.html', args)
