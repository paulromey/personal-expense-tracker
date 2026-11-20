
import sqlite3


DATABASE_NAME = "database/expenses.db"


def get_connection():
    return sqlite3.connect(DATABASE_NAME)


def initialize_database():
    connection = get_connection()
    cursor = connection.cursor()

    # Create transactions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            transaction_date TEXT
        )
    """)

    # Check existing table columns
    cursor.execute("PRAGMA table_info(transactions)")
    columns = [column[1] for column in cursor.fetchall()]

    # Add transaction_date if it does not exist
    if "transaction_date" not in columns:
        cursor.execute("""
            ALTER TABLE transactions
            ADD COLUMN transaction_date TEXT
        """)

    # Assign today's date to old transactions
    cursor.execute("""
        UPDATE transactions
        SET transaction_date = DATE('now')
        WHERE transaction_date IS NULL
    """)

    connection.commit()
    connection.close()


def add_transaction(transaction_type, amount, category, description, transaction_date):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO transactions
        (type, amount, category, description, transaction_date)
        VALUES (?, ?, ?, ?, ?)
    """, (
        transaction_type,
        amount,
        category,
        description,
        transaction_date
    ))

    connection.commit()
    connection.close()


def get_all_transactions():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM transactions")

    transactions = cursor.fetchall()

    connection.close()

    return transactions
