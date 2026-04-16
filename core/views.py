from django.shortcuts import render


def home(request):
    return render(request, "startseite.html")


def transaktionen(request):
    return render(request, "transaktionen.html")


def kontostand(request):
    return render(request, "kontostand.html")


def abheben(request):
    return render(request, "abheben.html")


def pin(request):
    return render(request, "pin.html")
