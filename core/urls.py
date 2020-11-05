from django.contrib import admin
from django.urls import include, path

from dashboard import urls as dashboard_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(dashboard_urls)),
]
