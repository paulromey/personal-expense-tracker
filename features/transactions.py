
from database.db import get_all_transactions


def search_transactions(keyword):
    transactions = get_all_transactions()

    results = [
        transaction
        for transaction in transactions
        if keyword.lower() in transaction[4].lower()
        or keyword.lower() in transaction[3].lower()
    ]

    return results


def filter_transactions(transaction_type):
    transactions = get_all_transactions()

    results = [
        transaction
        for transaction in transactions
        if transaction[1].lower() == transaction_type.lower()
    ]

    return results
