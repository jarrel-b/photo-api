from django.contrib import admin
from django.urls import include, path

from photocatalog import CURRENT_VERSION, views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.hello),
    path(f"{CURRENT_VERSION}/checkout", include("checkout.urls")),
    path(f"{CURRENT_VERSION}/catalog", include("photos.urls")),
]
