from django.urls import path

from . import views

urlpatterns = [
    path("", views.unit_rates, name="dashboard"),
    path("consumption", views.home_consumption, name="home_consumption"),
]
