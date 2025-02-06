from django.templatetags.static import static
from django.core.cache import cache
from .models import Title, MetaTag
import logging

logger = logging.getLogger(__name__)

def seo_data(request):
    current_url = request.path

    # Получаем Title
    title = Title.objects.filter(url=current_url).first()
    if not title:
        logger.warning(f'Не найден Title для URL: {current_url}')
        title = {'title_page': 'Default Title'}

    # Получаем MetaTag
    metatag = MetaTag.objects.filter(url=current_url).first()
    if metatag:
        metatag = {
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
            'description': metatag.og_description,
        }
    else:
        logger.warning(f'Не найден MetaTag для URL: {current_url}')
        metatag = {
            'og_image': 'Default Og:image',
            'og_image_secure_url': 'Default Og:image:secure_url',
            'og_image_width': '1200',
            'og_image_height': '630',
            'vk_image': 'Default vk:image',
            'og_image_alt': 'Default og:image:alt',
            'og_image_type': 'Default og:image:type',
            'og_type': 'Default Og:type',
            'og_title': 'Default Og:title',
            'og_description': 'Default Og:description',
            'og_url': 'Default example.ru',
            'og_site_name': 'Default Site name',
            'og_locale': 'ru_RU',
            'description': 'Default Description',
        }

    return {'title': title, 'metatag': metatag}