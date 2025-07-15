import sqlite3
import database as db

if __name__ == "__main__":
    # Connect to DB
    file_name = "data.db"
    conn = db.connect_DB(file_name)

    if conn:
        cursor = conn.cursor()
        # Insert into account_type table
        account_types = [
            ("Debit",),
            ("Credit",),
            ("Savings",),
            ("Investing",)
        ]
        cursor.executemany("INSERT INTO account_type (type) VALUES (?)",
            account_types)
        #conn.commit()
        
        conn.close()
