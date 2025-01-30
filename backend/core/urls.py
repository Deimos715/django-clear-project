from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticViewSitemap
from django.conf.urls.static import static
from . import views


handler404 = views.error_404

sitemaps = {
    'static': StaticViewSitemap,
}

urlpatterns = [
    path('auth/admin/', admin.site.urls),
    path('', include('src.main.urls', namespace='main')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', include('robots.urls'), name='robots'),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
