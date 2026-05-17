import json
from datetime import datetime
from functools import wraps
from pathlib import Path

from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

DATA_FILE = Path(__file__).resolve().parent.parent / 'Data' / 'Nutzer.json'
TRANSACTIONS_FILE = Path(__file__).resolve().parent.parent / 'Data' / 'transaktionen.json'


def load_users():
    try:
        return json.loads(DATA_FILE.read_text(encoding='utf-8'))
    except Exception:
        return []


def save_users(users):
    try:
        DATA_FILE.write_text(json.dumps(users, indent=2, ensure_ascii=False), encoding='utf-8')
    except Exception:
        pass


def load_transactions():
    try:
        data = TRANSACTIONS_FILE.read_text(encoding='utf-8').strip()
        if not data:
            return []
        return json.loads(data)
    except Exception:
        return []


def save_transactions(transactions):
    try:
        TRANSACTIONS_FILE.write_text(json.dumps(transactions, indent=2, ensure_ascii=False), encoding='utf-8')
    except Exception:
        pass


def get_user_by_rfid(uid):
    uid = str(uid or '').strip()
    if not uid:
        return None
    for user in load_users():
        if str(user.get('rfid', '')).strip() == uid:
            return user
    return None


def require_login(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('rfid_user'):
            return redirect('ausgeloggt')
        return view(request, *args, **kwargs)
    return wrapper


@require_login
def home(request):
    return render(request, 'startseite.html', {
        'logged_in': bool(request.session.get('rfid_user')),
        'rfid_user': request.session.get('rfid_user'),
    })


@require_login
def transaktionen(request):
    user = request.session.get('rfid_user')
    transactions = []
    if user:
        transactions = [
            item for item in load_transactions()
            if str(item.get('rfid', '')) == str(user.get('rfid', ''))
        ]
        transactions.sort(key=lambda item: item.get('timestamp', ''), reverse=True)
    return render(request, 'transaktionen.html', {
        'transactions': transactions,
        'user': user,
    })


@require_login
def kontostand(request):
    user = request.session.get('rfid_user')
    return render(request, 'kontostand.html', {
        'user': user,
        'balance': user.get('kontostand') if user else None,
    })


@require_login
def abheben(request):
    return render(request, 'abheben.html')


@require_login
def pin(request):
    return render(request, 'pin.html')


def ausgeloggt(request):
    return render(request, 'ausgeloggt.html', {
        'logged_in': bool(request.session.get('rfid_user')),
    })


def logout_view(request):
    request.session.pop('rfid_user', None)
    request.session.flush()
    return redirect('ausgeloggt')


@csrf_exempt
def abheben_api(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Nur POST erlaubt.'}, status=405)

    user = request.session.get('rfid_user')
    if not user:
        return JsonResponse({'success': False, 'error': 'Nicht eingeloggt.'}, status=403)

    try:
        payload = json.loads(request.body.decode('utf-8') or '{}')
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Ungültiges JSON.'}, status=400)

    amount_raw = str(payload.get('amount', '')).strip()
    pin = str(payload.get('pin', '')).strip()
    if not amount_raw:
        return JsonResponse({'success': False, 'error': 'Betrag fehlt.'}, status=400)

    try:
        amount = float(amount_raw.replace(',', '.'))
    except ValueError:
        return JsonResponse({'success': False, 'error': 'Ungültiger Betrag.'}, status=400)

    if amount <= 0:
        return JsonResponse({'success': False, 'error': 'Betrag muss größer null sein.'}, status=400)

    if not pin or len(pin) != 4 or not pin.isdigit():
        return JsonResponse({'success': False, 'error': 'PIN muss vierstellig sein.'}, status=400)

    users = load_users()
    target_user = None
    for idx, stored in enumerate(users):
        if str(stored.get('rfid', '')).strip() == str(user.get('rfid', '')).strip():
            target_user = (idx, stored)
            break

    if target_user is None:
        return JsonResponse({'success': False, 'error': 'Nutzer nicht gefunden.'}, status=404)

    idx, stored = target_user
    if str(stored.get('pin', '')) != pin:
        return JsonResponse({'success': False, 'error': 'PIN ist falsch.'}, status=403)

    current_balance = float(stored.get('kontostand', 0))
    if amount > current_balance:
        return JsonResponse({'success': False, 'error': 'Nicht genug Guthaben.'}, status=400)

    new_balance = round(current_balance - amount, 2)
    users[idx]['kontostand'] = new_balance
    save_users(users)

    updated_user = request.session['rfid_user'].copy()
    updated_user['kontostand'] = new_balance
    request.session['rfid_user'] = updated_user
    request.session.modified = True

    transactions = load_transactions()
    transactions.append({
        'rfid': str(stored.get('rfid', '')).strip(),
        'user': stored.get('user', ''),
        'amount': -round(amount, 2),
        'description': 'Geld abgehoben',
        'date': datetime.now().strftime('%d.%m.%Y'),
        'time': datetime.now().strftime('%H:%M'),
        'timestamp': datetime.now().isoformat(),
    })
    save_transactions(transactions)

    return JsonResponse({'success': True, 'balance': new_balance})


@csrf_exempt
def rfid_login(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Nur POST erlaubt.'}, status=405)

    try:
        payload = json.loads(request.body.decode('utf-8') or '{}')
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Ungültiges JSON.'}, status=400)

    uid = str(payload.get('uid', '')).strip()
    if not uid:
        return JsonResponse({'success': False, 'error': 'UID darf nicht leer sein.'}, status=400)

    user = get_user_by_rfid(uid)
    if not user:
        return JsonResponse({'success': False, 'error': 'Keine passende Nutzer-ID gefunden.'}, status=404)

    request.session['rfid_user'] = {
        'user': user.get('user'),
        'kontostand': user.get('kontostand'),
        'rfid': user.get('rfid'),
    }
    return JsonResponse({'success': True, 'user': user.get('user')})


    try:
        amount = float(amount_raw.replace(',', '.'))
    except ValueError:
        return JsonResponse({'success': False, 'error': 'Ungültiger Betrag.'}, status=400)

    if amount <= 0:
        return JsonResponse({'success': False, 'error': 'Betrag muss größer null sein.'}, status=400)

    if not pin or len(pin) != 4 or not pin.isdigit():
        return JsonResponse({'success': False, 'error': 'PIN muss vierstellig sein.'}, status=400)

    users = load_users()
    target_user = None
    for idx, stored in enumerate(users):
        if str(stored.get('rfid', '')).strip() == str(user.get('rfid', '')).strip():
            target_user = (idx, stored)
            break

    if target_user is None:
        return JsonResponse({'success': False, 'error': 'Nutzer nicht gefunden.'}, status=404)

    idx, stored = target_user
    if str(stored.get('pin', '')) != pin:
        return JsonResponse({'success': False, 'error': 'PIN ist falsch.'}, status=403)

    current_balance = float(stored.get('kontostand', 0))
    if amount > current_balance:
        return JsonResponse({'success': False, 'error': 'Nicht genug Guthaben.'}, status=400)

    new_balance = round(current_balance - amount, 2)
    users[idx]['kontostand'] = new_balance
    save_users(users)

    updated_user = request.session['rfid_user'].copy()
    updated_user['kontostand'] = new_balance
    request.session['rfid_user'] = updated_user
    request.session.modified = True

    transactions = load_transactions()
    transactions.append({
        'rfid': str(stored.get('rfid', '')).strip(),
        'user': stored.get('user', ''),
        'amount': -round(amount, 2),
        'description': 'Geld abgehoben',
        'date': datetime.now().strftime('%d.%m.%Y'),
        'time': datetime.now().strftime('%H:%M'),
        'timestamp': datetime.now().isoformat(),
    })
    save_transactions(transactions)

    return JsonResponse({'success': True, 'balance': new_balance})


@csrf_exempt
def rfid_login(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Nur POST erlaubt.'}, status=405)

    try:
        payload = json.loads(request.body.decode('utf-8') or '{}')
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Ungültiges JSON.'}, status=400)

    uid = str(payload.get('uid', '')).strip()
    if not uid:
        return JsonResponse({'success': False, 'error': 'UID darf nicht leer sein.'}, status=400)

    user = get_user_by_rfid(uid)
    if not user:
        return JsonResponse({'success': False, 'error': 'Keine passende Nutzer-ID gefunden.'}, status=404)

    request.session['rfid_user'] = {
        'user': user.get('user'),
        'kontostand': user.get('kontostand'),
        'rfid': user.get('rfid'),
    }
    return JsonResponse({'success': True, 'user': user.get('user')})

    