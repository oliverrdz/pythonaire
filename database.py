import sqlite3

def connect_DB(db_name):
    """ 
    Connects or creates a DB with name db_name
    """
    try:
        conn = sqlite3.connect(db_name)
        print(f"Connected to {db_name}.")
    except sqlite3.Error as error:
        print(f"Falied to connect to {db_name}.", error)
    if conn:
        return conn
    else:
        return null

if __name__ == "__main__":
    # Connect or create to DB
    file_name = "data.db"
    conn = connect_DB(file_name)

    if conn:
        cursor = conn.cursor() 

        # Create table account_type
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS account_type (
        type_id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
        type varchar(100)
        )
        """)
        print("Table account_type created")

        #Create table accounts
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS accounts(
        account_id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
        type_id integer NOT NULL,
        total float NOT NULL,
        FOREIGN KEY (type_id) REFERENCES account_type(type_id)
        )
        """)
        print("Table accounts created")

        # Create table transactions
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
        transaction_id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
        date datetime DEFAULT CURRENT_TIMESTAMP,
        account_id integer NOT NULL,
        ammount_added float NOT NULL,
        notes text,
        FOREIGN KEY (account_id) REFERENCES accounts(account_id)
        )
        """)
        print("Table transactions created")


        conn.close()


