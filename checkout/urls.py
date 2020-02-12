from django.urls import path

from . import views

urlpatterns = [
    path("", views.purchase_print, name="purchase-print"),
    path("print-sizes", views.list_sizes, name="list-sizes"),
]
