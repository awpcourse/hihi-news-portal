# Create your views here.

from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect

from news_portal.models import News, Category
from news_portal.forms import NewsItemCommentForm

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