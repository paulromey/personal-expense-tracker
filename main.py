from datetime import date

from database.db import get_all_transactions

from database.db import (
    initialize_database,
    add_transaction as save_transaction,
    get_all_transactions
)

from features.categories import (
    INCOME_CATEGORIES,
    EXPENSE_CATEGORIES
)

from features.transactions import (
    search_transactions,
    filter_transactions
)

from features.reports import monthly_report, category_report

from features.transactions import search_transactions


def display_menu():
    print("\n===== PERSONAL EXPENSE TRACKER =====")
    print("1. Add Income")
    print("2. Add Expense")
    print("3. View Transactions")
    print("4. View Financial Summary")
    print("5. Monthly Financial Report")
    print("6. Expense Breakdown by Category")
    print("7. Search Transactions")
    print("8. Filter Transactions")
    print("9. Exit")


def view_summary():
    print("\n===== FINANCIAL SUMMARY =====")

    transactions = get_all_transactions()

    total_income = sum(
        transaction[2]
        for transaction in transactions
        if transaction[1] == "Income"
    )

    total_expenses = sum(
        transaction[2]
        for transaction in transactions
        if transaction[1] == "Expense"
    )

    balance = total_income - total_expenses

    print(f"Total Income: PHP {total_income:,.2f}")
    print(f"Total Expenses: PHP {total_expenses:,.2f}")
    print("------------------------------")
    print(f"Remaining Balance: PHP {balance:,.2f}")


def add_transaction(transaction_type):
    print(f"\n===== ADD {transaction_type.upper()} =====")

    try:
        amount = float(input("Enter amount (PHP): "))

        if not 0 < amount <= 100000000:
            print("Amount must be greater than zero and not exceed PHP 100,000,000.")
            return

        categories = (
            INCOME_CATEGORIES
            if transaction_type == "Income"
            else EXPENSE_CATEGORIES
        )

        print("\nAvailable Categories:")

        for index, category_name in enumerate(categories, start=1):
            print(f"{index}. {category_name}")

        category_choice = int(input("Select category: "))

        if category_choice < 1 or category_choice > len(categories):
            print("Invalid category selection.")
            return

        category = categories[category_choice - 1]

        description = input("Enter description: ").strip()

        if not description:
            print("Description cannot be empty.")
            return

        if len(description) > 100:
            print("Description cannot exceed 100 characters.")
            return

        transaction_date = date.today().isoformat()

        save_transaction(
            transaction_type,
            amount,
            category,
            description,
            transaction_date
        )

        print(f"{transaction_type} successfully recorded!")

    except ValueError:
        print("Invalid input. Please try again.")


def view_transactions():
    print("\n===== TRANSACTION HISTORY =====")

    transactions = get_all_transactions()

    if not transactions:
        print("No transactions recorded yet.")
        return

    for transaction in transactions:
        print(f"\nTransaction #{transaction[0]}")
        print(f"Type: {transaction[1]}")
        print(f"Amount: PHP {transaction[2]:,.2f}")
        print(f"Category: {transaction[3]}")
        print(f"Description: {transaction[4]}")
        print(f"Date: {transaction[5]}")


def search_transaction_menu():
    print("\n===== SEARCH TRANSACTIONS =====")

    keyword = input("Enter description or category to search: ").strip()

    if not keyword:
        print("Search keyword cannot be empty.")
        return

    results = search_transactions(keyword)

    if not results:
        print("No matching transactions found.")
        return

    print(f"\nFound {len(results)} matching transaction(s):")

    for transaction in results:
        print(f"\nTransaction #{transaction[0]}")
        print(f"Type: {transaction[1]}")
        print(f"Amount: PHP {transaction[2]:,.2f}")
        print(f"Category: {transaction[3]}")
        print(f"Description: {transaction[4]}")
        print(f"Date: {transaction[5]}")


def filter_transaction_menu():
    print("\n===== FILTER TRANSACTIONS =====")
    print("1. Income")
    print("2. Expense")

    choice = input("Select transaction type: ")

    if choice == "1":
        transaction_type = "Income"
    elif choice == "2":
        transaction_type = "Expense"
    else:
        print("Invalid selection.")
        return

    results = filter_transactions(transaction_type)

    if not results:
        print(f"No {transaction_type.lower()} transactions found.")
        return

    print(f"\n===== {transaction_type.upper()} TRANSACTIONS =====")

    for transaction in results:
        print(f"\nTransaction #{transaction[0]}")
        print(f"Amount: PHP {transaction[2]:,.2f}")
        print(f"Category: {transaction[3]}")
        print(f"Description: {transaction[4]}")
        print(f"Date: {transaction[5]}")


def main():
    while True:
        display_menu()

        choice = input("Enter your choice: ")

        if choice == "1":
            add_transaction("Income")

        elif choice == "2":
            add_transaction("Expense")

        elif choice == "3":
            view_transactions()

        elif choice == "4":
            view_summary()

        elif choice == "5":
            try:
                year = int(input("Enter year (YYYY): "))
                month = int(input("Enter month (1-12): "))

                if month < 1 or month > 12 or year < 1:
                    print("Invalid year or month.")
                    continue

                monthly_report(year, month)

            except ValueError:
                print("Please enter valid numbers.")

        elif choice == "6":
            try:
                year = int(input("Enter year (YYYY): "))
                month = int(input("Enter month (1-12): "))

                if month < 1 or month > 12 or year < 1:
                    print("Invalid year or month.")
                    continue

                category_report(year, month)

            except ValueError:
                print("Please enter valid numbers.")
                
        elif choice == "7":
            search_transaction_menu()

        elif choice == "8":
            filter_transaction_menu()

        elif choice == "9":
            print("Thank you for using Expense Tracker!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    initialize_database()
    main()
