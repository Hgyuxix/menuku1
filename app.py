from flask import Flask, render_template, request
import qrcode
from io import BytesIO
import base64
from dotenv import load_dotenv
import os

load_dotenv()
MIDTRANS_SERVER_KEY = os.getenv("MIDTRANS_SERVER_KEY")
import requests
import json
from datetime import datetime

def create_midtrans_qris(total_amount, order_id):
    api_url = "https://api.sandbox.midtrans.com/v2/charge"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {MIDTRANS_SERVER_KEY.encode('utf-8').decode('latin1')}"
    }
    payload = {
        "payment_type": "qris",
        "transaction_details": {
            "order_id": order_id,
            "gross_amount": total_amount
        }
    }

    response = requests.post(api_url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error Midtrans: {response.text}")


app = Flask(__name__)

# Menu caffeshop
menu = {
    "Espresso": 20000,
    "Latte": 25000,
    "Cappuccino": 30000,
    "Mocha": 35000,
    "Tea": 15000,
    "Cake Slice": 20000,
}

# Pesanan pelanggan
order = {}
# Nomor rekening penerima
account_number = "366201016699505 (Bank BRI)"

@app.route("/")
def index():
    return render_template("index.html", menu=menu, order=order)

@app.route("/add", methods=["POST"])
def add_to_order():
    item = request.form.get("item")
    quantity = int(request.form.get("quantity", 1))
    if item in menu:
        order[item] = order.get(item, 0) + quantity
    return render_template("index.html", menu=menu, order=order)

@app.route("/clear")
def clear_order():
    order.clear()
    return render_template("index.html", menu=menu, order=order)

@app.route("/bayar")
def Pay():
    # Hitung total biaya
    total = sum(menu[item] * quantity for item, quantity in order.items())
    order_id = f"order_{datetime.now().strftime('%Y%m%d%H%M%S')}"

    try:
        # Panggil API Midtrans
        midtrans_response = create_midtrans_qris(total, order_id)
        qris_url = midtrans_response["actions"][0]["url"]  # URL QRIS

        # Tampilkan QRIS di halaman
        return render_template("Bayar.html", total=total, qris_url=qris_url, order_id=order_id)
    except Exception as e:
        return f"Terjadi kesalahan: {e}"

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    # Ambil data notifikasi
    order_id = data.get("order_id")
    status = data.get("transaction_status")

    # Verifikasi status pembayaran
    if status == "settlement":
        print(f"Pembayaran untuk {order_id} berhasil.")
    elif status == "pending":
        print(f"Pembayaran untuk {order_id} sedang menunggu.")
    elif status in ["cancel", "deny", "expire"]:
        print(f"Pembayaran untuk {order_id} gagal atau dibatalkan.")

    return "OK", 200
