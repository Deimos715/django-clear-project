from django.contrib import admin, messages
from .models import MetaTag
from django.db import IntegrityError
import copy



@admin.register(MetaTag)
class MetaTagAdmin(admin.ModelAdmin):
    list_display = ['name_page', 'url', 'created', 'updated']
    actions = ['duplicate_selected'] # Копирование выбранных метатегов

    fieldsets = [
        ('Название страницы', {'fields': ['name_page']}),
        ('Заголовок страницы', {'fields': ['title_page']}),
        ('Стандартные метатеги', {'fields': ['description']}),
        ('Opengraph метатеги', {'fields': ['og_type', 'og_title', 'og_description', 'og_url', 'og_site_name', 'og_locale']}),
        ('Адрес страницы', {'fields': ['url']}),
    ]

    # Копирование выбранных метатегов
    def duplicate_selected(self, request, queryset):
        count = 0
        for obj in queryset:
            obj_copy = copy.copy(obj)
            obj_copy.pk = None
            obj_copy.name_page = f"{obj.name_page} (копия)"

            # Уникализируем url
            base_url = obj.url or '/'
            if base_url == '/':
                base_url = '/copy'

            new_url = base_url.rstrip('/') + '-copy'
            i = 1
            while MetaTag.objects.filter(url=new_url).exists():
                new_url = f"{base_url.rstrip('/')}-copy{i}"
                i += 1

            obj_copy.url = new_url

            try:
                obj_copy.save()
                count += 1
            except IntegrityError:
                continue  # Если вдруг всё равно не прошла валидация, пропускаем

        self.message_user(request, f"Скопировано {count} метатегов", messages.SUCCESS)

    duplicate_selected.short_description = "Скопировать выбранные Метатеги"

    def message_user(self, request, message, level=messages.INFO, extra_tags='',
                    fail_silently=False):
        pass

    def save_model(self, request, obj, form, change):
        messages.add_message(request, messages.INFO, 'Все изменения успешно сохранены')
        obj.save()

    show_close_button = True

    # save_as = True # Кнопка "Сохранить как новый объект"
