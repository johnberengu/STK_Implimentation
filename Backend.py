from flask import Flask, request, jsonify
import requests
import base64
import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow all origins for testing

consumer_key = "Zxaaz9xOgdJX1CzgszvY33ejWoNxG9qne5TsVj22zG72Ccg0"
consumer_secret = "fr1I8zIqJPnDSyyNPItL4TRx4vWp2GsjRTqLFGm4kGgJPrziA0z6FoLgGKsGZDkP"
shortcode = "174379" 
passkey = "bfb279f9aa9bdbcf15e97dd71a467cd2e0c893059b10f78c1b9c049c0a2c3c99"

def get_access_token():
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(url, auth=(consumer_key, consumer_secret))
    return response.json().get('access_token')

def get_password():
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    data = shortcode + passkey + timestamp
    password = base64.b64encode(data.encode()).decode()
    return password, timestamp

@app.route('/stkpush', methods=['POST'])
def stkpush():
    data = request.json
    phone = data.get('phone')
    amount = data.get('amount', 1)
    callback_url = data.get('callback_url', 'https://webhook.site/your-unique-url')
    access_token = get_access_token()
    password, timestamp = get_password()
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "BusinessShortCode": shortcode,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone,
        "PartyB": shortcode,
        "PhoneNumber": phone,
        "CallBackURL": callback_url,
        "AccountReference": "Test123",
        "TransactionDesc": "Testing Daraja"
    }
    res = requests.post(
        "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest",
        json=payload,
        headers=headers
    )
    return jsonify(res.json())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)