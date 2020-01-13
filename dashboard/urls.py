from django.urls import path

from . import views

urlpatterns = [
    path("", views.unit_rates, name="dashboard"),
    path("consumption", views.consumption, name="consumption"),
]
