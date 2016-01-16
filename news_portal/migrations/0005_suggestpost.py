# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-16 15:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news_portal', '0004_news_author'),
    ]

    operations = [
        migrations.CreateModel(
            name='SuggestPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100, unique=True)),
                ('link', models.URLField(max_length=10000, unique=True)),
            ],
            options={
                'ordering': ['-description'],
                'verbose_name_plural': 'SuggestNews',
            },
        ),
    ]