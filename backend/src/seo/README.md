Модуль SEO для сайта
1. Подключаем приложение в INSTALLED_APPS, к примеру 'src.seo.apps.SeoConfig',
2. В TEMPLATES добавляем контекстный процессор 'src.seo.context_processors.seo_data',
3. В модель метатегов добавлена универсальная связь с разными моделями (GenericForeignKey)
4. Логика обработки зашита в файле context_processors.py, для стандатных страниц, к примеру "Главная" - адрес будет как "/", "О нас" - адрес будет как "/about-us", для детальных страниц работает универсальная связь и заполнять адрес не требуется
5. В нужной модели, где должна быть связь с метатегами добавляем поле. к примеру meta_tags = models.OneToOneField(MetaTag, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Мета-теги")
6. В файле views.py нужной модели Получаем SEO-данные seo = seo_data(request, instance=article), в контексте выводим **seo
7. В главном шаблоне обозначаем блок тегов:
 - <title>{% block title %}{% endblock %}</title>
 - {% block metatags %}{% endblock %}
8. В каждом шаблоне выводим теги:
 - {% block title %}{{ metatag.title_page }}{% endblock %}
 - {% block metatags %}
    <meta property="og:image" content="{{ metatag.og_image }}">
    <meta property="og:image:secure_url" content="{{ metatag.og_image_secure_url }}"/>
    <meta property="og:image:width" content="{{ metatag.og_image_width }}">
    <meta property="og:image:height" content="{{ metatag.og_image_height }}">
    <meta property="vk:image" content="{{ metatag.vk_image }}">
    <meta property="og:image:alt" content="{{ metatag.og_image_alt }}"/>
    <meta property="og:image:type" content="{{ metatag.og_image_type }}"/>
    <meta property="og:type" content="{{ metatag.og_type }}">
    <meta property="og:title" content="{{ metatag.og_title }}">
    <meta property="og:description" content="{{ metatag.og_description }}">
    <meta property="og:url" content="{{ metatag.og_url }}{{ request.path }}">
    <meta property="og:site_name" content="{{ metatag.og_site_name }}">
    <meta property="og:locale" content="{{ metatag.og_locale }}">
    <meta name="description" content="{{ metatag.description }}">
{% endblock %}
