#!/usr/bin/env python3
import argparse
import json
import os
from datetime import datetime
from typing import List, Dict

DATA_FILE = "expenses.json"

def load_expenses() -> List[Dict]:
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_expenses(expenses: List[Dict]) -> None:
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(expenses, f, indent=2)

def generate_id(expenses: List[Dict]) -> int:
    if not expenses:
        return 1
    return max(exp["id"] for exp in expenses) + 1

def add_expense(description: str, amount: float) -> None:
    if amount <= 0:
        print("Error: Amount must be greater than zero")
        return

    expenses = load_expenses()
    expense = {
        "id": generate_id(expenses),
        "date": datetime.now().strftime("%Y-%m-%d"),
        "description": description,
        "amount": amount,
    }
    expenses.append(expense)
    save_expenses(expenses)

    print(f"Expense added successfully (ID: {expense['id']})")

def update_expense(expense_id: int, description: str, amount: float) -> None:
    expenses = load_expenses()

    for exp in expenses:
        if exp["id"] == expense_id:
            if description:
                exp["description"] = description
            if amount is not None:
                if amount <= 0:
                    print("Error: Amount must be greater than zero")
                    return
                exp["amount"] = amount

            save_expenses(expenses)
            print("Expense updated successfully")
            return

    print("Error: Expense ID not found")

def delete_expense(expense_id: int) -> None:
    expenses = load_expenses()
    new_expenses = [exp for exp in expenses if exp["id"] != expense_id]

    if len(new_expenses) == len(expenses):
        print("Error: Expense ID not found")
        return

    save_expenses(new_expenses)
    print("Expense deleted successfully")

def list_expenses() -> None:
    expenses = load_expenses()

    if not expenses:
        print("No expenses found")
        return

    print("ID  Date        Description           Amount")
    print("--  ----------  --------------------  ------")
    for exp in expenses:
        print(
            f"{exp['id']:<3} {exp['date']}  {exp['description']:<20}  ${exp['amount']}"
        )

def summary(month: int | None = None) -> None:
    expenses = load_expenses()
    total = 0

    for exp in expenses:
        date = datetime.strptime(exp["date"], "%Y-%m-%d")
        if month is None or date.month == month:
            total += exp["amount"]

    if month:
        month_name = datetime(1900, month, 1).strftime("%B")
        print(f"Total expenses for {month_name}: ${total}")
    else:
        print(f"Total expenses: ${total}")

def main() -> None:
    parser = argparse.ArgumentParser(description="Expense Tracker CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Add
    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("--description", required=True)
    add_parser.add_argument("--amount", required=True, type=float)

    # Update
    update_parser = subparsers.add_parser("update")
    update_parser.add_argument("--id", required=True, type=int)
    update_parser.add_argument("--description")
    update_parser.add_argument("--amount", type=float)

    # Delete
    delete_parser = subparsers.add_parser("delete")
    delete_parser.add_argument("--id", required=True, type=int)

    # List
    subparsers.add_parser("list")

    # Summary
    summary_parser = subparsers.add_parser("summary")
    summary_parser.add_argument("--month", type=int)

    args = parser.parse_args()

    if args.command == "add":
        add_expense(args.description, args.amount)
    elif args.command == "update":
        update_expense(args.id, args.description, args.amount)
    elif args.command == "delete":
        delete_expense(args.id)
    elif args.command == "list":
        list_expenses()
    elif args.command == "summary":
        summary(args.month)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
