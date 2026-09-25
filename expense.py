"""
Simple Expense Tracker
-----------------------
A command-line app to add, view, filter, and summarize expenses.
Data is stored persistently in a local JSON file (expenses.json).
"""

import json
import os
from datetime import datetime

DATA_FILE = "expenses.json"


def load_expenses():
    """Load expenses from the JSON file, or return an empty list."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []


def save_expenses(expenses):
    """Save the list of expenses back to the JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(expenses, f, indent=2)


def add_expense(expenses):
    try:
        amount = float(input("Amount: ₹"))
        category = input("Category (e.g. Food, Travel, Bills): ").strip().title()
        description = input("Description: ").strip()
        date_str = input("Date (YYYY-MM-DD) [leave blank for today]: ").strip()
        date = date_str if date_str else datetime.now().strftime("%Y-%m-%d")

        expense = {
            "amount": amount,
            "category": category,
            "description": description,
            "date": date,
        }
        expenses.append(expense)
        save_expenses(expenses)
        print("✅ Expense added.\n")
    except ValueError:
        print("❌ Invalid amount. Please enter a number.\n")


def view_expenses(expenses):
    if not expenses:
        print("No expenses recorded yet.\n")
        return

    print(f"\n{'Date':<12}{'Category':<15}{'Amount':<10}Description")
    print("-" * 55)
    for e in sorted(expenses, key=lambda x: x["date"]):
        print(f"{e['date']:<12}{e['category']:<15}₹{e['amount']:<9.2f}{e['description']}")
    print()


def view_summary(expenses):
    if not expenses:
        print("No expenses recorded yet.\n")
        return

    total = sum(e["amount"] for e in expenses)
    print(f"\n💰 Total spent: ₹{total:.2f}")

    by_category = {}
    for e in expenses:
        by_category[e["category"]] = by_category.get(e["category"], 0) + e["amount"]

    print("\nBy category:")
    for cat, amt in sorted(by_category.items(), key=lambda x: -x[1]):
        print(f"  {cat:<15} ₹{amt:.2f}")
    print()


def filter_by_category(expenses):
    category = input("Enter category to filter by: ").strip().title()
    filtered = [e for e in expenses if e["category"] == category]
    if not filtered:
        print(f"No expenses found for category '{category}'.\n")
        return
    view_expenses(filtered)


def delete_expense(expenses):
    view_expenses(expenses)
    if not expenses:
        return
    try:
        index = int(input("Enter the row number to delete (1-based, from list above): ")) - 1
        sorted_expenses = sorted(expenses, key=lambda x: x["date"])
        if 0 <= index < len(sorted_expenses):
            removed = sorted_expenses.pop(index)
            expenses.remove(removed)
            save_expenses(expenses)
            print(f"🗑️ Deleted: {removed['description']} (₹{removed['amount']:.2f})\n")
        else:
            print("❌ Invalid row number.\n")
    except ValueError:
        print("❌ Please enter a valid number.\n")


def main():
    expenses = load_expenses()

    menu = """
=== Expense Tracker ===
1. Add expense
2. View all expenses
3. View summary (total + by category)
4. Filter by category
5. Delete an expense
6. Exit
"""
    while True:
        print(menu)
        choice = input("Choose an option (1-6): ").strip()

        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            view_expenses(expenses)
        elif choice == "3":
            view_summary(expenses)
        elif choice == "4":
            filter_by_category(expenses)
        elif choice == "5":
            delete_expense(expenses)
        elif choice == "6":
            print("Goodbye! 👋")
            break
        else:
            print("❌ Invalid choice, try again.\n")


if __name__ == "__main__":
    main()
