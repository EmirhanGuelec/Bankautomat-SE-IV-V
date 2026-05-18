from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json

JSON_PATH = settings.BASE_DIR / "Data" / "Nutzer.json"

logged_in = False
current_user = None


def ausgeloggt(request):

    if logged_in:
        return redirect("/startseite/")

    return render(request, "ausgeloggt.html")


@csrf_exempt
def rfid_login(request):

    global logged_in
    global current_user

    data = json.loads(request.body)

    uid = str(data["uid"])

    with open(JSON_PATH, "r", encoding="utf-8") as f:
        users = json.load(f)

    for user in users:

        if user["uid"] == uid:

            logged_in = True
            current_user = user

            print("Login:", user["user"])

            return JsonResponse({
                "success": True
            })

    return JsonResponse({
        "success": False
    })


def logout(request):

    global logged_in
    global current_user

    logged_in = False
    current_user = None

    return redirect("/ausgeloggt/")


def startseite(request):

    if not logged_in:
        return redirect("/ausgeloggt/")

    return render(request, "startseite.html", {
        "user": current_user
    })


def abheben(request):

    if not logged_in:
        return redirect("/ausgeloggt/")

    return render(request, "abheben.html")


def pin(request):

    if not logged_in:
        return redirect("/ausgeloggt/")

    return render(request, "pin.html")


def kontostand(request):

    if not logged_in:
        return redirect("/ausgeloggt/")

    return render(request, "kontostand.html", {
        "user": current_user
    })


def transaktionen(request):

    if not logged_in:
        return redirect("/ausgeloggt/")

    return render(request, "transaktionen.html")