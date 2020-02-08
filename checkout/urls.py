from django.urls import path

from . import views

urlpatterns = [
    path("", views.purchase_print, name="purchase-print"),
]
