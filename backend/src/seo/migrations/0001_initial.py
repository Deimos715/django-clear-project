# Generated by Django 5.1.3 on 2025-02-09 11:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='MetaTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_page', models.CharField(max_length=50, verbose_name='Название страницы')),
                ('title_page', models.TextField(max_length=80, verbose_name='Заголовок страницы (максимум 80 символов)')),
                ('description', models.TextField(max_length=190, verbose_name='Description (максимум 190 символов)')),
                ('og_type', models.CharField(choices=[('website', 'website'), ('article', 'article'), ('book', 'book'), ('profile', 'profile'), ('music', 'music'), ('video', 'video')], default='website', max_length=12, verbose_name='Og:type')),
                ('og_title', models.CharField(max_length=60, verbose_name='Og:title (максимум 60 символов)')),
                ('og_description', models.TextField(max_length=190, verbose_name='Og:description (максимум 190 символов)')),
                ('og_url', models.CharField(default='https://webdevlabs.ru', max_length=30, verbose_name='Og:url')),
                ('og_site_name', models.CharField(default='WebDevLabs - Разработка современных сайтов, уникального дизайна, SEO-продвижению и создание PBN сайтов под ключ', max_length=120, verbose_name='Og:site_name')),
                ('og_locale', models.CharField(choices=[('en_US', 'en_US'), ('ru_RU', 'ru_RU')], default='ru_RU', max_length=30, verbose_name='Og:locale')),
                ('url', models.CharField(blank=True, max_length=30, null=True, unique=True, verbose_name='Адрес страницы (не заполняется для детальных страниц)')),
                ('object_id', models.PositiveIntegerField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Добавлено')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Обновлено')),
                ('content_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
            options={
                'verbose_name': 'Метатег',
                'verbose_name_plural': 'Метатеги',
            },
        ),
    ]
