
import unittest

from features.transactions import (
    search_transactions,
    filter_transactions
)


class TestTransactions(unittest.TestCase):

    def test_search_transactions_returns_list(self):
        results = search_transactions("Food")
        self.assertIsInstance(results, list)

    def test_filter_transactions_returns_list(self):
        results = filter_transactions("Income")
        self.assertIsInstance(results, list)

    def test_filter_income_returns_only_income(self):
        results = filter_transactions("Income")

        for transaction in results:
            self.assertEqual(transaction[1], "Income")

    def test_filter_expense_returns_only_expenses(self):
        results = filter_transactions("Expense")

        for transaction in results:
            self.assertEqual(transaction[1], "Expense")


if __name__ == "__main__":
    unittest.main()
