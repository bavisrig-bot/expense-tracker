from flask import Flask, render_template, request, redirect
import json
import os
from datetime import datetime

app = Flask(__name__)

DATA_FILE = "expenses.json"


def load_expenses():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []

    return []


def save_expenses(expenses):
    with open(DATA_FILE, "w") as f:
        json.dump(expenses, f, indent=2)


@app.route("/")
def home():
    expenses = load_expenses()

    total = sum(expense["amount"] for expense in expenses)

    return render_template(
        "index.html",
        expenses=expenses,
        total=total
    )


@app.route("/add", methods=["POST"])
def add():
    expenses = load_expenses()

    amount = float(request.form["amount"])
    category = request.form["category"].strip().title()
    description = request.form["description"].strip()

    date = request.form["date"]

    if not date:
        date = datetime.now().strftime("%Y-%m-%d")

    expense = {
        "amount": amount,
        "category": category,
        "description": description,
        "date": date
    }

    expenses.append(expense)

    save_expenses(expenses)

    return redirect("/")


@app.route("/delete/<int:index>")
def delete(index):
    expenses = load_expenses()

    if 0 <= index < len(expenses):
        expenses.pop(index)
        save_expenses(expenses)

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
