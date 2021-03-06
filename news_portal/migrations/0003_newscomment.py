# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-16 07:43
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('news_portal', '0002_auto_20160105_1031'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=100)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('news_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='news_portal.News')),
            ],
            options={
                'ordering': ['date_added'],
            },
        ),
    ]
