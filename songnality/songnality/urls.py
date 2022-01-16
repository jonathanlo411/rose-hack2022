from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

# Pages
from landing.views import landing, about, pinfo
from songselect.views import songselect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing, name="landing"),
    path('about', about, name="about"),
    path('pinfo', pinfo, name="pinfo"),
    path('songselect', songselect, name="songselect")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
