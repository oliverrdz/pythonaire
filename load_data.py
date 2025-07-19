import sqlite3
import generate_db as db

def account_type(conn, cursor, data):
    """
    Insert data into account_type table
    """
    account_types = 0
    try:
        cursor.execute("""
            SELECT type FROM account_type
        """)
        account_types = cursor.fetchall()
    except:
        pass

    if account_types:
        if (data[0],) in account_types:
            print(f"Account type {data[0]} already exists.")
            return 0
    cursor.execute("INSERT INTO account_type (type) VALUES (?)", data)
    conn.commit()
    print(f"Added account type {data[0]}.")

def account(conn, cursor, data):
    """
    Inserts data into accounts table
    """
    accounts = 0
    try:
        cursor.execute("""
            SELECT name from accounts
        """)
        accounts = cursor.fetchall()[0][0]
    except:
        pass

    if accounts:
        if data[0] in accounts:
            print(f"Account {data[0]} already exists.")
            return 0
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
    #conn.row_factory = sqlite3.Row

    acc_type = ("Credit",)
    name = "Bank1"
    initial_ammount = 0
    ammount_added = 100
    note = "Transfer"
    
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


    if 0:
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
