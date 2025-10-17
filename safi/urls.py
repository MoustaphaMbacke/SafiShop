
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

#from ajax_select import urls as ajax_select_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('user/', include('userauths.urls')),
    path("useradmin/", include("useradmin.urls")),

    path("ckeditor5/", include('django_ckeditor_5.urls')),
 #   path("admin/lookups/", include(ajax_select_urls)),



    path('blog/', include('blog.urls', namespace='blog')),
]



if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)