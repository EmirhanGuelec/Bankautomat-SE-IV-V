
from django.urls import path
from . import views

urlpatterns = [

    path("ausgeloggt/", views.ausgeloggt, name="ausgeloggt"),

    path("rfid-login/", views.rfid_login, name="rfid_login"),

    path("logout/", views.logout, name="logout"),

    path("startseite/", views.startseite, name="startseite"),

    path("abheben/", views.abheben, name="abheben"),

    path("pin/", views.pin, name="pin"),

    path("kontostand/", views.kontostand, name="kontostand"),

    path("transaktionen/", views.transaktionen, name="transaktionen"),
]
