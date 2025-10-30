from flask import Flask, request
import requests
import random

app = Flask(__name__)

# 🟢 ADRES TWOJEGO TELEFONU Z APLIKACJĄ SMS GATEWAY
PHONE_IP = "http://192.168.8.161:8080"  # ← tu wpiszesz swój adres IP z telefonu

@app.route('/send_sms', methods=['POST'])
def send_sms():
    data = request.get_json()
    phone = data.get("phone")

    if not phone:
        return {"status": "error", "message": "Brak numeru telefonu"}, 400

    # Generowanie prostego kodu rabatowego
    code = str(random.randint(1000, 9999))
    message = f"Dziękujemy za opinię! Twój kod rabatowy do Bistro Zosieńka: {code}"

    # Wysyłanie SMS przez Twój telefon (SMS Gateway)
    try:
        r = requests.post(f"{PHONE_IP}/send", json={"number": phone, "message": message})
        if r.status_code == 200:
            return {"status": "ok", "message": f"SMS wysłany do {phone}"}
        else:
            return {"status": "error", "message": "Błąd przy wysyłaniu SMS-a"}, 500
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
