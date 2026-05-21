
from django.urls import path
from . import views

urlpatterns = [

    path("ausgeloggt/", views.ausgeloggt, name="ausgeloggt"),

    path("rfid-login/", views.rfid_login, name="rfid_login"),

    path("logout/", views.logout, name="logout"),

    path("startseite/", views.startseite, name="startseite"),

    path("abheben/", views.abheben, name="abheben"),

    path("pin/", views.pin, name="pin"),

    path("changepin/",views.changepin, name="changepin"),

    path("confirmpin/",views.confirmpin, name="confirmpin"),

    path("kontostand/", views.kontostand, name="kontostand"),

    path("transaktionen/", views.transaktionen, name="transaktionen"),
    
    
]
