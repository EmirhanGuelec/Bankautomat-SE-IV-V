from django.urls import path

from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('api/rfid-login/', views.rfid_login, name='rfid_login'),
    path('api/abheben/', views.abheben_api, name='abheben_api'),
    path('logout/', views.logout_view, name='logout'),
    path('transaktionen/', views.transaktionen, name='transaktionen'),
    path('kontostand/', views.kontostand, name='kontostand'),
    path('abheben/', views.abheben, name='abheben'),
    path('pin/', views.pin, name='pin'),
    path('ausgeloggt/', views.ausgeloggt, name='ausgeloggt'),
]
