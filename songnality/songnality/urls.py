from django.contrib import admin
from django.urls import path

# Pages
from landing.views import landing

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing, name="landing")
]
