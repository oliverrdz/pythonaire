import sqlite3
import generate_db as db

if __name__ == "__main__":
    file_name = "sqlite.db"
    conn = db.connect_DB(file_name)

    if conn:
        # Converts rows into dictionaries:
        conn.row_factory = sqlite3.Row 
        cursor = conn.cursor()
        
        # Read account_type table
        cursor.execute("SELECT * FROM account_type")
        rows = cursor.fetchall()
        account_type = [dict(row) for row in rows]
        print("Account types available:")
        for x in account_type:
            print(x)

        # Read accounts table
        #cursor.execute("SELECT * FROM accounts")
        cursor.execute("""
            SELECT accounts.name, account_type.type_name, accounts.total
            FROM accounts
            JOIN account_type ON accounts.account_id = account_type.type_id
        """)
        rows = cursor.fetchall()
        accounts = [dict(row) for row in rows]
        print("Accounts available:")
        for x in accounts:
            print(x)

        # Read transactions table
        cursor.execute("""
            SELECT transactions.date, accounts.name, transactions.ammount_added,
            transactions.notes
            FROM transactions
            JOIN accounts ON transactions.account_id = accounts.account_id
        """)
        rows = cursor.fetchall()
        transactions = [dict(row) for row in rows]
        print("Transactions recorded:")
        for x in transactions:
            print(x)

        conn.close()
