from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

class SuggestPost(models.Model):
    description = models.CharField(max_length=100,unique=True)
    link = models.URLField(max_length=10000,unique=True)

    class Meta:
        ordering = ['-description']
        verbose_name_plural = 'SuggestNews'

    def __unicode__(self):
        return self.description


class News(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    body = models.TextField()
    posted = models.DateField(db_index=True, auto_now_add=True)
    category = models.ForeignKey('Category')
    author = models.ForeignKey(User, editable=False)
    count_hit = models.IntegerField(default=0)
    def increase_count_hit(self):
        self.count_hit += 1

    class Meta:
        ordering = ['-posted']
        verbose_name_plural = 'News'

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('news_details', None, { 'slug': self.slug })

class NewsAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not change and not obj.author:
            obj.author = request.user
            obj.save()

class Category(models.Model):
    title = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, db_index=True)

    class Meta:
        ordering = ['title']
        verbose_name_plural = 'Categories'

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('view_category', None, { 'slug': self.slug })

class NewsComment(models.Model):
    text = models.TextField(max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User)
    news_post = models.ForeignKey(News, related_name='comments')

    class Meta:
        ordering = ['date_added']

    def __unicode__(self):
        return u'{} @ {}'.format(self.author, self.date_added)
