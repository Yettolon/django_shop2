
from django.contrib import admin
from django.urls import path,include
from . import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    
    
    path('api/v1/',include('api.urls')),
    path('api-auth/',include('rest_framework.urls')),
    path('', include('kind.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
]


if settings.DEBUG:

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)