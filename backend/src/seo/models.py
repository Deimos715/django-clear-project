from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

TYPE_CHOICES = (
    ('website', 'website'),
    ('article', 'article'),
    ('book', 'book'),
    ('profile', 'profile'),
    ('music', 'music'),
    ('video', 'video'),
)

LOCALE_CHOICES = (
    ('en_US', 'en_US'),
    ('ru_RU', 'ru_RU'),
)

class MetaTag(models.Model):
    # Название страницы
    name_page = models.CharField(max_length=50, verbose_name='Название страницы')
    
    # Заголовок страницы
    title_page = models.TextField(max_length=80, verbose_name='Заголовок страницы (максимум 80 символов)')
    
    # Стандартные метатеги
    description = models.TextField(max_length=190, verbose_name='Description (максимум 190 символов)')
    
    # Opengraph метатеги
    og_type = models.CharField(max_length=12, choices=TYPE_CHOICES, default='website', verbose_name='Og:type')
    og_title = models.CharField(max_length=60, verbose_name='Og:title (максимум 60 символов)')
    og_description = models.TextField(max_length=190, verbose_name='Og:description (максимум 190 символов)')
    og_url = models.CharField(max_length=30, default='https://example.ru', verbose_name='Og:url')
    og_site_name = models.CharField(max_length=120, default='og site name', verbose_name='Og:site_name')
    og_locale = models.CharField(max_length=30, choices=LOCALE_CHOICES, default='ru_RU', verbose_name='Og:locale')
    url = models.CharField(max_length=30, unique=True, blank=True, null=True,
                        verbose_name='Адрес страницы (не заполняется для детальных страниц)')
    
    # Универсальная связь с разными моделями (GenericForeignKey)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    
    created = models.DateTimeField(auto_now_add=True, verbose_name='Добавлено')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    class Meta:
        verbose_name = 'Метатег'
        verbose_name_plural = 'Метатеги'

    def __str__(self):
        return self.name_page
