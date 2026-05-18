import requests
from mfrc522 import SimpleMFRC522

# RFID Reader starten
reader = SimpleMFRC522()

# Django Server
SERVER_URL = "http://192.168.178.51:8000/rfid-login/"

print("Warte auf RFID Karte...")

while True:

    # Wartet bis Karte erkannt wird
    uid = None
    uid, text = reader.read()

    uid = str(uid)

    print("Karte erkannt:", uid)

    try:

        # UID an Server senden
        response = requests.post(
            SERVER_URL,
            json={
                "uid": uid
            }
        )

        # Antwort anzeigen
        print(response.json())

    except Exception as e:

        print("Server nicht erreichbar:", e)
