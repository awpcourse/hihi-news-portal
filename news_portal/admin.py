from django.contrib import admin
from news_portal import models

class NewsAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not change and obj.author_id is None:
            obj.author = request.user
            obj.save()

admin.site.register(models.News, NewsAdmin)
admin.site.register(models.Category)
admin.site.register(models.SuggestPost)
admin.site.register(models.NewsComment)