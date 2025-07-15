import sqlite3
import generate_db as db

def account_type(cursor):
    """
    Insert into account_type table
    """
    account_types = [
        ("Debit",),
        ("Credit",),
        ("Savings",),
        ("Investing",)
    ]
    cursor.executemany("INSERT INTO account_type (type) VALUES (?)",
        account_types)
    conn.commit()
    print("Populated account_type table")

def account(conn, cursor, data):
    """
    Inserts data into accounts table
    """
    cursor.execute("""
    INSERT INTO accounts (name, type_id, initial_ammount) \
    VALUES (?, ?, ?)
    """, data)
    conn.commit()
    print("Populated accounts table")
        
def transactions(conn, cursor, data):
    """
    Inserts data into the transactions table
    """
    cursor.execute("""
        INSERT INTO transactions (account_id, ammount_added, notes) 
        VALUES (?, ?, ?)
    """, data)
    conn.commit()
    print("Populated transactions table")

if __name__ == "__main__":
    # Connect to DB
    file_name = "sqlite.db"
    conn = db.connect_DB(file_name)

    if conn:
        acc_type = ("Debit",)
        name = "Bank1"
        initial_ammount = 0
        ammount_added = 100
        note = "First transfer"

        cursor = conn.cursor()

        # Load account_type data
        account_type(cursor)

        # Find type_id from accounts table
        cursor.execute("SELECT type_id FROM account_type \
                        WHERE type = ?", acc_type)
        type_id = cursor.fetchall()[0][0]

        # Load accounts data
        data = (name, type_id, initial_ammount)
        account(conn, cursor, data)

        # Find account_id from accounts table
        cursor.execute("""
            SELECT account_id FROM accounts
            WHERE name = ?
        """, (name,))
        account_id = cursor.fetchall()[0][0]

        # Load transactions data
        data = (account_id, ammount_added, note)
        transactions(conn, cursor, data)
        
        
        conn.close()
