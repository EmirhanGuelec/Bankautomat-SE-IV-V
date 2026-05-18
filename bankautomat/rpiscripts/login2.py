import requests

SERVER_URL = "http://192.168.178.51:8000/rfid-login/"

uid = "647199131442"

response = requests.post(
    SERVER_URL,
    json={
        "uid": uid
    }
)

print(response.text)
