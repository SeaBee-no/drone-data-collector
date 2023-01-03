from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include, re_path
from . import settings
from .views import *

from .views import StaticViewSitemap

sitemaps = {
    'static': StaticViewSitemap
}


urlpatterns = [
    path('accounts/register/', ExtraFieldRegistrationView.as_view(), name='registration_register'),
    path(r'accounts/', include('registration.backends.default.urls')),
    path('admin/', admin.site.urls),
    path(r'', include('dmc.urls')),
    path(r'', include('home.urls')),

    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT )
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.site_header = "Welcome to FARE Admin Area"
admin.site.site_title = "Welcome to FARE Portal "
admin.site.index_title = "List of all editable data node"