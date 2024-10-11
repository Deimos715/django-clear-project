from django.contrib import admin, messages
from .models import MetaTag, Title


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ['name_page', 'url', 'created', 'updated']

    fieldsets = [
        ('Название страницы', {'fields': ['name_page']}),
        ('Заголовок страницы', {'fields': ['title_page']}),
        ('Адрес страницы', {'fields': ['url']}),
    ]

    def message_user(self, request, message, level=messages.INFO, extra_tags='',
                    fail_silently=False):
        pass

    def save_model(self, request, obj, form, change):
        messages.add_message(request, messages.INFO, 'Все изменения успешно сохранены')
        obj.save()

    show_close_button = True


@admin.register(MetaTag)
class MetaTagAdmin(admin.ModelAdmin):
    list_display = ['name_page', 'url', 'created', 'updated']

    fieldsets = [
        ('Название страницы', {'fields': ['name_page']}),
        ('Стандартные метатеги', {'fields': ['description']}),
        ('Opengraph метатеги', {'fields': ['og_type', 'og_title', 'og_description', 'og_url', 'og_site_name',
                                        'og_locale']}),
        ('Адрес страницы', {'fields': ['url']}),
    ]

    def message_user(self, request, message, level=messages.INFO, extra_tags='',
                    fail_silently=False):
        pass

    def save_model(self, request, obj, form, change):
        messages.add_message(request, messages.INFO, 'Все изменения успешно сохранены')
        obj.save()

    show_close_button = True
