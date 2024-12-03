from flask import Flask, render_template, request

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

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)