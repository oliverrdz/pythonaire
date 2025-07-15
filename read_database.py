import sqlite3
import database as db

if __name__ == "__main__":
    file_name = "data.db"
    conn = db.connect_DB(file_name)

    if conn:
        cursor = conn.cursor()
        
        # SELECT query
        cursor.execute("SELECT * FROM account_type")
        accounts = cursor.fetchall()

        for entry in accounts:
            print(entry)

        conn.close()
