from django.contrib import admin
from news_portal import models

admin.site.register(models.News)
admin.site.register(models.Category)