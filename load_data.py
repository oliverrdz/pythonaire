import sqlite3
import generate_db as db

def total_wealth(conn, cursor):
    """
    Calculates the total wealth from the accounts table
    """

    try:
        cursor.execute("""
            SELECT total FROM accounts
        """)
        totals = cursor.fetchall()
        total = 0
        for x in totals:
            total = total + x[0]
        return total
    except:
        pass

def account_type(conn, cursor, data):
    """
    Insert data into account_type table
    """
    account_names = 0
    try:
        cursor.execute("""
            SELECT type_name FROM account_type
        """)
        account_names = cursor.fetchall()
    except:
        pass

    if account_names:
        if (data[0],) in account_names:
            print(f"Account type {data[0]} already exists.")
            return 0
    cursor.execute("""
        INSERT INTO account_type (type_name, type) 
        VALUES (?,?)""", data)
    conn.commit()
    print(f"Added account type {data[0]}.")

def account(conn, cursor, data):
    """
    Inserts data into accounts table
    """
    data = data + (0,) # Add initial ammount of 0 to total
    accounts = 0
    
    # Check if account already exists:
    try:
        cursor.execute("""
            SELECT name from accounts
        """)
        accounts = cursor.fetchall()
    except:
        pass
    if accounts:
        if (data[0],) in accounts:
            print(f"Account {data[0]} already exists.")
            return 0

    # Add new account:
    cursor.execute("""
    INSERT INTO accounts (name, type_id, total) \
    VALUES (?, ?, ?)
    """, data)
    conn.commit()
    print(f"Added account {data[0]}.")
        
def transactions(conn, cursor, data):
    """
    Inserts data into the transactions table
    """

    # Check if account type is "Negative" to make the added amount negative
    acc_type = 0
    try:
        cursor.execute("""
            SELECT type FROM account_type
            WHERE type_id = (?)
        """, (data[0],))
        acc_type = cursor.fetchall()[0][0]
    except:
        pass
    if acc_type == "Negative":
        # Ensure ammount added is always negative:
        ammount_added = -abs(data[1])
        data = (data[0], ammount_added, data[2])
        #data = data[:2] + ammount_added
    else:
        ammount_added = abs(data[1])
        data = (data[0], ammount_added, data[2])
        #data = data[:2] + ammount_added

    # Find last ammount and name from accounts table:
    cursor.execute("""
        SELECT total, name FROM accounts
        WHERE account_id = ?
    """, (data[0],))
    last_ammount, acc_name = cursor.fetchall()[0]

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
    print(f"Added {ammount_added} to account {acc_name}")

if __name__ == "__main__":
    # Connect to DB
    file_name = "sqlite.db"
    conn = db.connect_DB(file_name)
    #conn.row_factory = sqlite3.Row

    acc_type = "Negative"
    acc_name = "Credit"
    name = "Bank1"
    initial_ammount = 0
    ammount_added = 100
    note = "Payment"
    
    cursor = conn.cursor()

    # Load account_type data
    #account_type(conn, cursor, (acc_name, acc_type))

    # Find type_id from accounts table
    data = (acc_name, acc_type)
    cursor.execute("SELECT type_id FROM account_type \
                    WHERE type_name = ?", (acc_name,))
    type_id = cursor.fetchall()[0][0]

    # Load accounts data
    data = (name, type_id)
    #account(conn, cursor, data)

    # Find account_id from accounts table
    cursor.execute("""
        SELECT account_id FROM accounts
        WHERE name = ?
    """, (name,))
    account_id = cursor.fetchall()[0][0]

    # Load transactions data
    cursor.execute("""
        SELECT account_id FROM accounts
        WHERE name = (?)
    """, (name,))
    account_id = cursor.fetchall()[0][0]
    data = (account_id, ammount_added, note)
    #transactions(conn, cursor, data)

    print("Total wealth:", total_wealth(conn, cursor))
    conn.close()
