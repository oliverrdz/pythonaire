import sqlite3

def create_DB(db_name):
    try:
        conn = sqlite3.connect(file_name)
        print(f"Database {file_name} created.")
    except:
        print(f"Database {file_name} not created.")

def connect_DB(db_name):
    try:
        conn = sqlite3.connect(db_name)
        print(f"Connected to {db_name}.")
    except sqlite3.Error as error:
        print(f"Falied to connect to {db_name}.", error)
    finally:
        if conn:
            conn.close()
            print(f"Database {file_name} closed.")


if __name__ == "__main__":
    file_name = "data.db"

    create_DB(file_name)
    connect_DB(file_name)

