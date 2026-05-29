from flask import Flask, request, redirect, render_template
import sqlite3

app = Flask(__name__)
DB = "orders.db"

def init_db():
    with sqlite3.connect(DB) as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name     TEXT NOT NULL,
                email         TEXT NOT NULL,
                phone         TEXT,
                ship_line1    TEXT NOT NULL,
                ship_city     TEXT NOT NULL,
                ship_zip      TEXT NOT NULL,
                delivery_date TEXT NOT NULL,
                card_number   TEXT NOT NULL,
                card_expiry   TEXT NOT NULL,
                card_cvv      TEXT NOT NULL,
                bill_line1    TEXT NOT NULL,
                bill_city     TEXT NOT NULL,
                bill_zip      TEXT NOT NULL,
                discount_code TEXT,
                terms         INTEGER NOT NULL,
                marketing     INTEGER DEFAULT 0,
                created_at    DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

@app.route("/")
def index():
    return render_template("form.html")

@app.route("/checkout", methods=["POST"])
def checkout():
    f = request.form
    errors = []

    required = {
        "full_name": "Full name",
        "email": "Email",
        "ship_line1": "Shipping address",
        "ship_city": "Shipping city",
        "ship_zip": "Shipping ZIP",
        "delivery_date": "Delivery date",
        "card_number": "Card number",
        "card_expiry": "Expiration date",
        "card_cvv": "CVV",
        "bill_line1": "Billing address",
        "bill_city": "Billing city",
        "bill_zip": "Billing ZIP",
    }

    for field, label in required.items():
        if not f.get(field, "").strip():
            errors.append(f"{label} is required")

    if not f.get("terms"):
        errors.append("You must accept the terms and conditions")

    if errors:
        return render_template("error.html", errors=errors)

    with sqlite3.connect(DB) as db:
        db.execute("""
            INSERT INTO orders (
                full_name, email, phone, ship_line1, ship_city, ship_zip,
                delivery_date, card_number, card_expiry, card_cvv,
                bill_line1, bill_city, bill_zip,
                discount_code, terms, marketing
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            f["full_name"].strip(),
            f["email"].strip(),
            f.get("phone", "").strip() or None,
            f["ship_line1"].strip(),
            f["ship_city"].strip(),
            f["ship_zip"].strip(),
            f["delivery_date"],
            f["card_number"].strip(),
            f["card_expiry"].strip(),
            f["card_cvv"].strip(),
            f["bill_line1"].strip(),
            f["bill_city"].strip(),
            f["bill_zip"].strip(),
            f.get("discount_code", "").strip() or None,
            1,
            1 if f.get("marketing") else 0
        ))

    return redirect("/success")

@app.route("/success")
def success():
    return render_template("success.html")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
