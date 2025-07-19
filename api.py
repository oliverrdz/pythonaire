import sqlite3

def setup(db_name="pythonaire.db"):
    """
    Creates db and tables
    """
    db = DB()
    db.create_tables(db_name)
    db.close()

class DB:
    """
    New database 
    """
    def connect(self, db_name):
        """
        Connects to database db_name
        """
        try:
            self.conn = sqlite3.connect(db_name)
            # Needs to be added according to ChatGPT 4o
            self.conn.execute("PRAGMA foreign_Keys = ON;")
            self.conn.row_factory = sqlite3.Row
            print(f"\nConnected to {db_name}.")
            self.cursor = self.conn.cursor()
            return 1
        except sqlite3.Error as e:
            print(f"\nFailed to connect to {db_name}.", e)
            return 0

    def create_tables(self, db_name):
        """
        Creates all required tables

        Pending:
        * Check if tables already exist
        """
        if not self.connect(db_name):
            print(f"Can't connect to database {db_name}")
            return 0
        # Create table account_type:
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS account_type (
        type_id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
        type_name varchar(100),
        type varchar(100)
        )
        """)
        print("Table account_type created")

        # Create table accounts
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS accounts(
        account_id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
        name text NOT NULL,
        type_id integer NOT NULL,
        total float NOT NULL,
        FOREIGN KEY (type_id) REFERENCES account_type(type_id)
        )
        """)
        print("Table accounts created")

        # Create table transactions
        self.cursor.execute("""
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


    def close(self):
        """
        Closes database
        """
        self.conn.close()
        print(f"\nDatabase closed.\n")



if __name__ == "__main__":
    import api 

    # Create database
    db_name = "sqlite.db"
    setup()
    #db = api.DB()
    #db.create_tables(db_name)
    #db.close()

    # Delete database
    if 0:
        import os
        file_name = db_name
        if os.path.isfile(file_name):
            os.remove(file_name)
            print(f"{file_name} has been deleted.")
        else:
            print(f"{file_name} does not exist.")
