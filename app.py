from flask import Flask, render_template, request
import qrcode
from io import BytesIO
import base64

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
def pay():
    # Hitung total biaya
    total = sum(menu[item] * quantity for item, quantity in order.items())
    # Buat data QR Code (misalnya mencantumkan rekening dan total)
    qr_data = f"Transfer Rp{total} ke rekening: {account_number}"
    qr = qrcode.QRCode()
    qr.add_data(qr_data)
    qr.make(fit=True)

    # Simpan QR Code ke dalam memori
    img = qr.make_image(fill="black", back_color="white")
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    qr_code_base64 = base64.b64encode(buffered.getvalue()).decode()

    return render_template("Bayar.html", total=total, qr_code=qr_code_base64, account_number=account_number)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
