# Create your views here.

from news_portal.forms import NewsItemCommentForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from news_portal.models import News, Category
from django.shortcuts import render_to_response, get_object_or_404
from news_portal.forms import UserLoginForm
from django.shortcuts import redirect, render


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **kwargs):
        view = super(LoginRequiredMixin, cls).as_view(**kwargs)
        return login_required(view)


def index(request):
    return render_to_response('index.html', {
        'categories': Category.objects.all(),
        'posts': News.objects.all()[:5]
    })

def view_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    return render_to_response('view_category.html', {
        'category': category,
        'posts': News.objects.filter(category=category)
    })

def news_details(request, slug):
    news_item = News.objects.get(slug=slug)
    if request.method == 'GET':
        form = NewsItemCommentForm()
        context = {
            'post': news_item,
            'form': form,
        }
        return render(request, 'view_post.html', context)
    # elif request.method == 'POST':
    #     form = NewsItemCommentForm(request.POST)
    #     if form.is_valid():
    #         text = form.cleaned_data['text']
    #         comment = NewsComment(text=text, post=post, author=request.user)
    #         comment.save()
    #     return redirect('news_details', slug=slug)


def login_view(request):
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
                'message': 'Wrong username or password!'
            }
            return render(request, 'login.html', context)
        else:
            login(request, user)
            return redirect('index')


def logout_view(request):
    logout(request)
    return redirect('login')