import json
import os
from datetime import datetime
from django.shortcuts import render


DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Data')


def load_json(filename):
    path = os.path.join(DATA_DIR, filename)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


def save_json(filename, data):
    with open(os.path.join(DATA_DIR, filename), 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def home(request):
    return render(request, "startseite.html")


def transaktionen(request):
    user = request.session.get('user')
    transaktionen = load_json('Transaktionen.json')
    if user:
        transaktionen = [t for t in transaktionen if t.get('user') == user]
    return render(request, "transaktionen.html", {'transaktionen': transaktionen})


def kontostand(request):
    user = request.session.get('user')
    kontostand = 0
    if user:
        for n in load_json('Nutzer.json'):
            if n.get('user') == user:
                kontostand = n.get('kontostand', 0)
                break
    return render(request, "kontostand.html", {'kontostand': kontostand})


def abheben(request):
    user = request.session.get('user')
    kontostand = 0
    fehler = None
    erfolg = None
    
    if request.method == 'POST':
        try:
            betrag = float(request.POST.get('betrag', 0))
            nutzer = load_json('Nutzer.json')
            
            for n in nutzer:
                if n.get('user') == user:
                    if n.get('kontostand', 0) >= betrag and betrag > 0:
                        n['kontostand'] = n.get('kontostand', 0) - betrag
                        kontostand = n['kontostand']
                        save_json('Nutzer.json', nutzer)
                        
                        transaktionen = load_json('Transaktionen.json')
                        transaktionen.append({
                            'user': user,
                            'typ': 'Abhebung',
                            'betrag': -betrag,
                            'datum': datetime.now().strftime('%d.%m.%Y'),
                            'zeit': datetime.now().strftime('%H:%M')
                        })
                        save_json('Transaktionen.json', transaktionen)
                        erfolg = f"{betrag:.2f} € ausgezahlt"
                    else:
                        fehler = "Nicht genug Guthaben"
                    break
        except:
            fehler = "Ungultiger Betrag"
    
    if user:
        for n in load_json('Nutzer.json'):
            if n.get('user') == user:
                kontostand = n.get('kontostand', 0)
                break
    
    return render(request, "abheben.html", {'kontostand': kontostand, 'fehler': fehler, 'erfolg': erfolg})


def pin(request):
    return render(request, "pin.html")


def Login(request):
    user = request.session.get('user')
    if user:
        return render(request, "startseite.html")
    
    step = request.session.get('login_step', 0)
    fehler = None
    benutzer = None
    
    if request.method == 'POST':
        if step == 0:
            # Schritt 1: RFID
            rfid = request.POST.get('rfid', '').strip()
            for n in load_json('Nutzer.json'):
                if n.get('rfid') == rfid:
                    request.session['login_user'] = n.get('user')
                    request.session['login_step'] = 1
                    return render(request, "login.html", {'step': 1, 'benutzer': n.get('user')})
            fehler = "Karte nicht erkannt"
        
        elif step == 1:
            # Schritt 2: PIN
            login_user = request.session.get('login_user')
            pin = request.POST.get('pin', '')
            for n in load_json('Nutzer.json'):
                if n.get('user') == login_user and n.get('pin') == pin:
                    request.session['user'] = login_user
                    request.session.pop('login_user', None)
                    request.session.pop('login_step', None)
                    return render(request, "startseite.html")
            fehler = "Falsche PIN"
    
    request.session.pop('login_user', None)
    request.session.pop('login_step', None)
    
    return render(request, "login.html", {'step': 0, 'fehler': fehler})


def ausgeloggt(request):
    request.session.flush()
    return render(request, "ausgeloggt.html")


    