from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json

JSON_PATH = settings.BASE_DIR / "Data" / "Nutzer.json"

logged_in = False
current_user = None


def ausgeloggt(request):
    global JSON_PATH
    global logged_in
    global current_user
    if logged_in:
        return redirect("/startseite/")
    
    #ganzes if ding nur für testphase für manuelle verifizierung
    if request.method=="POST":  
        uid=request.POST.get("uid")
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            users = json.load(f)
        for u in users:
            if u["uid"]== uid:
                logged_in=True
                current_user=u
                return redirect("/startseite/")
            else:
                logged_in=False

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
    alter_kontostand=0
    if not logged_in:
        return redirect("/ausgeloggt/")
    
    if request.method=="POST":
        betrag=request.POST.get("betrag")

        with open(JSON_PATH, "r", encoding="utf-8") as f:
            users = json.load(f)

        for u in users:
            if u["uid"] == current_user["uid"]:
                alter_kontostand=u["kontostand"]
                neuer_kontostand= int(alter_kontostand) - int(betrag)
                u["kontostand"]=neuer_kontostand
                current_user["kontostand"]=neuer_kontostand

        with open(JSON_PATH, "w", encoding="utf-8") as f:
                json.dump(users, f, ensure_ascii=False, indent=4)

    return render(request, "abheben.html")


def pin(request):

    if not logged_in:
        return redirect("/ausgeloggt/")
    
    if request.method=="POST":
        alterpin=request.POST.get("AlterPin")
        
        if alterpin==current_user["pin"]:
            
            return render(request,"changepin.html")
        
        else:

            return render(request,"pin.html",{"error":"Falscher Pin"})
        
    return render(request, "pin.html")

def changepin(request):

    if not logged_in:
        return redirect("/ausgeloggt/")
    
    if request.method=="POST":
        
        neuerpin1=request.POST.get("Neuerpin")
        
    if not neuerpin1:
        return render(request,"changepin.html",{"error":"Bitte PIN erneut eingeben"})
    
    if neuerpin1:
        return render(request,"confirmpin.html",{"neuerpin":neuerpin1})
    
    return render(request,"changepin.html")

def confirmpin(request):

    if not logged_in:
        return redirect("/ausgeloggt/")
    
    if request.method=="POST":

        neuerpin2=request.POST.get("Neuerpin")
        neuerpin1=request.POST.get("erste_eingabe")

    if not neuerpin1 or not neuerpin2:

        return render(request,"changepin.html",{"error":"Bitte PIN erneut eingeben"})
    
    if neuerpin2==neuerpin1:

        with open(JSON_PATH, "r", encoding="utf-8") as f:
            users = json.load(f)

        for u in users:
            if u["uid"] == current_user["uid"]:
                u["pin"]=neuerpin1
                current_user["pin"]=neuerpin1

        with open(JSON_PATH, "w", encoding="utf-8") as f:
                json.dump(users, f, ensure_ascii=False, indent=4)
    
        return render(request,"pin.html",{"message":"PIN wurde Erfolgreich geändert"})
    else:
        return render(request,"changepin.html",{"error":"PINs stimmen nicht überein!"})

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