import sqlite3

def setup(db_name="pythonaire.db"):
    """
    Creates db and tables
    """
    db = DB()
    db.create_tables(db_name)
    db.generate_category_type()

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
            print(f"\nConnected to {db_name}.\n")
            self.cursor = self.conn.cursor()
            return 1
        except sqlite3.Error as e:
            print(f"\nFailed to connect to {db_name}.\n", e)
            return 0

    def create_tables(self, db_name):
        """
        Creates all required tables

        Pending:
        * Check if tables already exist
        """
        if not self.connect(db_name):
            print(f"\nCan't connect to database {db_name}\n")
            return 0

        # Create table category_type (e.g. Positive/Negative):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS category_type (
        cat_type_id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
        cat_type varchar(100)
        )""")
        print("Table category_type created")

        # Create table category (e.g. Debit, Credit, Savings, etc):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS category (
        cat_id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
        cat_name varchar(100),
        type_id integer NOT NULL,
        FOREIGN KEY (type_id) REFERENCES category_type(cat_type_id)
        )
        """)
        print("Table category created")

        # Create table accounts (e.g. Amex, Chase debit, etc)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS accounts(
        acc_id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
        acc_name text NOT NULL,
        cat_id integer NOT NULL,
        acc_total float NOT NULL,
        acc_notes text,
        FOREIGN KEY (cat_id) REFERENCES category(cat_id)
        )
        """)
        print("Table accounts created")

        # Create table transactions
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
        trans_id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
        trans_date datetime DEFAULT CURRENT_TIMESTAMP,
        acc_id integer NOT NULL,
        trans_amount float NOT NULL,
        trans_notes text,
        FOREIGN KEY (acc_id) REFERENCES accounts(acc_id)
        )
        """)
        print("Table transactions created")


    def generate_category_type(self):
        category_types = [
            ("Positive",),
            ("Negative",)
        ]
        self.cursor.executemany("""
            INSERT INTO category_type (cat_type)
            VALUES (?)
        """, category_types)
        self.conn.commit()
        

    def close(self):
        """
        Closes database
        """
        self.conn.close()
        print(f"\nDatabase closed.\n")



if __name__ == "__main__":
    import api 

    # Create database
    db_name = "pythonaire.db"
    setup()

    # Add account types

    # Delete database
    if 0:
        import os
        file_name = db_name
        if os.path.isfile(file_name):
            os.remove(file_name)
            print(f"{file_name} has been deleted.")
        else:
            print(f"{file_name} does not exist.")
