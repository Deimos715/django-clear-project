from django.db import models

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


class Title(models.Model):
    name_page = models.CharField(max_length=50, verbose_name='Название страницы')
    title_page = models.TextField(max_length=80, verbose_name='Заголовок страницы (максимум 80 символов)')
    url = models.CharField(max_length=30, unique=True, blank=True, null=True,
                        verbose_name='Адрес страницы (не заполняется для детальных страниц)')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Добавлено')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    class Meta:
        verbose_name = 'Заголовок'
        verbose_name_plural = 'Заголовки'

    def __str__(self):
        return self.name_page



class MetaTag(models.Model):
    name_page = models.CharField(max_length=50, verbose_name='Название страницы')
    # Стандартные метатеги
    description = models.TextField(max_length=190, verbose_name='Description (максимум 190 символов)')
    # Opengraph метатеги
    og_type = models.CharField(max_length=12, choices=TYPE_CHOICES, default='website', verbose_name='Og:type')
    og_title = models.CharField(max_length=60, verbose_name='Og:title (максимум 60 символов)')
    og_description = models.TextField(max_length=190, verbose_name='Og:description (максимум 190 символов)')
    og_url = models.CharField(max_length=30, default='https://webdevlabs.ru', verbose_name='Og:url')
    og_site_name = models.CharField(max_length=120, default='WebDevLabs - Разработка современных сайтов, уникального дизайна, SEO-продвижению и создание PBN сайтов под ключ', verbose_name='Og:site_name')
    og_locale = models.CharField(max_length=30, choices=LOCALE_CHOICES, default='ru_RU', verbose_name='Og:locale')
    url = models.CharField(max_length=30, unique=True, blank=True, null=True,
                        verbose_name='Адрес страницы (не заполняется для детальных страниц)')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Добавлено')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    class Meta:
        verbose_name = 'Метатег'
        verbose_name_plural = 'Метатеги'

    def __str__(self):
        return self.name_page
