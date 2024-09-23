from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('qb_app.urls')),
    path('api/', include('qb_app.api_urls')),
    path('manager/', include('manager_app.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


        