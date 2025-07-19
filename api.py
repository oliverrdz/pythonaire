import sqlite3

def connect(db_name):
    try:
        conn = sqlite3.connect(db_name)
        # Needs to be added according to ChatGPT 4o
        conn.execute("PRAGMA foreign_Keys = ON;")
        conn.row_factory = sqlite3.Row
        print(f"\nConnected to {db_name}.\n")
        return conn
    except sqlite3.Error as e:
        print(f"\nFailed to connect to {db_name}.", e)
        return 0

def close(conn):
    conn.close()
    print(f"\nDatabase closed.\n")

def read_account_types(conn):
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM account_type
    """)
    rows = cursor.fetchall()
    account_types = [dict(row) for row in rows]
    return account_types

def read_accounts(conn):
    cursor.execute("""
        SELECT accounts.name, account_type.type, accounts.total
        FROM accounts
        JOIN account_type ON accounts.account_id = account_type.type_id
    """)
    rows = cursor.fetchall()
    accounts = [dict(row) for row in rows]
    return accounts

if __name__ == "__main__":
    name = "sqlite.db"
    conn = connect(name)
    account_types = read_account_types(conn)
    for x in account_types:
        print(x)

    close(conn)
