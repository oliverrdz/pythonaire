import sqlite3
import generate_db as db

def account_type(conn, cursor, data):
    """
    Insert data into account_type table
    """
    cursor.execute("INSERT INTO account_type (type) VALUES (?)", data)
    conn.commit()
    print("Populated account_type table")

def account(conn, cursor, data):
    """
    Inserts data into accounts table
    """
    cursor.execute("""
    INSERT INTO accounts (name, type_id, total) \
    VALUES (?, ?, ?)
    """, data)
    conn.commit()
    print("Populated accounts table")
        
def transactions(conn, cursor, data):
    """
    Inserts data into the transactions table
    """
    cursor.execute("""
        SELECT total FROM accounts
        WHERE account_id = ?
    """, (data[0],))
    last_ammount = cursor.fetchall()[0][0]
    print(last_ammount)
    print(ammount_added)
    if 1:
        cursor.execute("""
            INSERT INTO transactions (account_id, ammount_added, notes) 
            VALUES (?, ?, ?)
        """, data)
        cursor.execute("""
            UPDATE accounts 
            SET total = ?
            where account_id = ?
        """, (ammount_added+last_ammount, data[0]))
        conn.commit()
        print("Populated transactions table")

if __name__ == "__main__":
    # Connect to DB
    file_name = "sqlite.db"
    conn = db.connect_DB(file_name)

    acc_type = ("Debit",)
    name = "Bank1"
    initial_ammount = 0
    ammount_added = 100
    note = "Transfer"
    
    if 1:
        cursor = conn.cursor()

        # Load account_type data
        account_type(conn, cursor, acc_type)

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
        account_id = 1
        data = (account_id, ammount_added, note)
        transactions(conn, cursor, data)


    conn.close()
