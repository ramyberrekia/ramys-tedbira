from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('recipes.urls', namespace='recipes')),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404='recipes.views.handle_or_404'
handler500='recipes.views.handle_or_500'