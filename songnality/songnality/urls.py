from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

# Pages
from landing.views import landing

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing, name="landing")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
