from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

admin.autodiscover()

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
]

# Эндпоинты для которых нужна мультиязычность
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),  # Авторизация и регистрация
    path('pages/', include('django.contrib.flatpages.urls')),  # FlatPages
    path('contact/', include("contact.urls")),
    path("", include("movies.urls")),
)

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
