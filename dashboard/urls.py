from django.urls import path

from . import views

urlpatterns = [
    path("", views.unit_rates_dashboard, name="dashboard"),
    path("consumption", views.consumption_dashboard, name="home_consumption"),
]
