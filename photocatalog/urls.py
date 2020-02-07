from django.contrib import admin
from django.urls import include, path

from photocatalog import CURRENT_VERSION

urlpatterns = [
    path("admin/", admin.site.urls),
    path(f"{CURRENT_VERSION}/catalog", include("photos.urls")),
]
