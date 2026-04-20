from django.urls import path

from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("transaktionen/", views.transaktionen, name="transaktionen"),
    path("kontostand/", views.kontostand, name="kontostand"),
    path("abheben/", views.abheben, name="abheben"),
    path("pin/", views.pin, name="pin"),
    path("login/", views.Login, name="login"),
    path("ausgeloggt/", views.ausgeloggt, name="ausgeloggt"),
]
