from django.templatetags.static import static
from django.contrib.contenttypes.models import ContentType
from .models import MetaTag
import logging

logger = logging.getLogger(__name__)

def seo_data(request, instance=None):
    """
    Получает SEO-данные для конкретной модели или по URL.
    :param request: HttpRequest
    :param instance: Опциональный объект модели (Portfolio, Article и т.д.)
    :return: Словарь с metatag
    """
    current_url = request.path
    logger.debug(f"🔍 Проверяем SEO для URL: {current_url}")

    # Инициализация переменных
    metatag = None

    # 1. Если передан объект, берем SEO-данные напрямую
    if instance:
        logger.debug(f"Ищем SEO-данные у объекта {instance.__class__.__name__} (ID: {instance.id})")

        # Проверяем, есть ли связанные SEO-данные
        if hasattr(instance, 'title') and instance.title:
            title = instance.title
            logger.debug(f"Найден Title: {title.title_page}")

        if hasattr(instance, 'meta_tags') and instance.meta_tags:
            metatag = instance.meta_tags
            logger.debug(f"Найден MetaTag: {metatag.og_title}")

    # 2. Если метатеги не найдены, ищем по URL
    if not metatag:
        logger.debug(f"🔍 Поиск MetaTag по URL: {current_url}")
        metatag = MetaTag.objects.filter(url=current_url).first()

    if not metatag:
        logger.warning(f'Не найден MetaTag для URL: {current_url}')
        metatag = MetaTag(
            title_page='Default title page',
            og_type='website',
            og_title='Default Og:title',
            og_description='Default Og:description',
            og_url=f'{request.scheme}://{request.get_host()}{current_url}',
            og_site_name='Default Site name',
            og_locale='ru_RU',
            description='Default Description',
        )

    # Формируем данные для метатегов
    seo_metatag = {
        'title_page': metatag.title_page,
        'og_image': f'{request.scheme}://{request.get_host()}{static("img/open_graph_preview.png")}',
        'og_image_secure_url': f'{request.scheme}://{request.get_host()}{static("img/open_graph_preview.png")}',
        'og_image_width': '1200',
        'og_image_height': '630',
        'vk_image': f'{request.scheme}://{request.get_host()}{static("img/open_graph_preview.png")}?format=vk',
        'og_image_alt': 'WebDevLabs разработка',
        'og_image_type': 'image/png',
        'og_type': metatag.og_type,
        'og_title': metatag.og_title,
        'og_description': metatag.og_description,
        'og_url': metatag.og_url,
        'og_site_name': metatag.og_site_name,
        'og_locale': metatag.og_locale,
        'description': metatag.description,
    }

    logger.debug(f"Итоговые данные: MetaTag={seo_metatag['og_title']}")

    return {
        'metatag': seo_metatag,
    }