from flask import Flask, render_template, request

app = Flask(__name__)

# Sample menu items
menu = [
    {"id": 1, "name": "Cappuccino", "price": 3.5},
    {"id": 2, "name": "Latte", "price": 4.0},
    {"id": 3, "name": "Espresso", "price": 2.5},
    {"id": 4, "name": "Croissant", "price": 2.0},
    {"id": 5, "name": "Bagel", "price": 3.0},
]

@app.route("/")
def index():
    return render_template("index.html", menu=menu)

@app.route("/order", methods=["POST"])
def order():
    order_items = request.form.getlist("item")
    order_total = sum(float(item.split("|")[1]) for item in order_items)
    return render_template("order.html", order_items=order_items, order_total=order_total)

if __name__ == "__main__":
    app.run(debug=True)