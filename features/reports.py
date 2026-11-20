
from database.db import get_all_transactions


def monthly_report(year, month):
    transactions = get_all_transactions()

    monthly_transactions = [
        transaction
        for transaction in transactions
        if transaction[5]
        and transaction[5][:7] == f"{year}-{month:02d}"
    ]

    total_income = sum(
        transaction[2]
        for transaction in monthly_transactions
        if transaction[1] == "Income"
    )

    total_expenses = sum(
        transaction[2]
        for transaction in monthly_transactions
        if transaction[1] == "Expense"
    )

    balance = total_income - total_expenses

    print(f"\n===== REPORT: {year}-{month:02d} =====")

    print(f"Total Income: PHP {total_income:,.2f}")
    print(f"Total Expenses: PHP {total_expenses:,.2f}")
    print("------------------------------")
    print(f"Remaining Balance: PHP {balance:,.2f}")

    if not monthly_transactions:
        print("No transactions found for this month.")


def category_report(year, month):
    transactions = get_all_transactions()

    category_totals = {}

    for transaction in transactions:
        transaction_date = transaction[5]

        if (
            transaction[1] == "Expense"
            and transaction_date
            and transaction_date[:7] == f"{year}-{month:02d}"
        ):
            category = transaction[3]
            amount = transaction[2]

            category_totals[category] = (
                category_totals.get(category, 0) + amount
            )

    print(f"\n===== EXPENSE BREAKDOWN: {year}-{month:02d} =====")

    if not category_totals:
        print("No expenses found for this month.")
        return

    total_expenses = sum(category_totals.values())

    for category, amount in sorted(
        category_totals.items(),
        key=lambda item: item[1],
        reverse=True
    ):
        percentage = (amount / total_expenses) * 100

        print(
            f"{category}: PHP {amount:,.2f} "
            f"({percentage:.1f}%)"
        )

    print("------------------------------")
    print(f"Total Expenses: PHP {total_expenses:,.2f}")
