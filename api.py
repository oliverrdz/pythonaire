import sqlite3

class DB:
    def connect(self, db_name):
        try:
            self.conn = sqlite3.connect(db_name)
            # Needs to be added according to ChatGPT 4o
            self.conn.execute("PRAGMA foreign_Keys = ON;")
            self.conn.row_factory = sqlite3.Row
            print(f"\nConnected to {db_name}.")
            return self.conn
        except sqlite3.Error as e:
            print(f"\nFailed to connect to {db_name}.", e)
            return 0

    def close(self):
        self.conn.close()
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
    import api 

    # Create database
    db_name = "sqlite.db"
    db = api.DB()
    conn = db.connect(db_name)
    db.close()

    # Delete database
    if 0:
        import os
        file_name = db_name
        if os.path.isfile(file_name):
            os.remove(file_name)
            print(f"{file_name} has been deleted.")
        else:
            print(f"{file_name} does not exist.")
