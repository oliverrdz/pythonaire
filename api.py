import sqlite3

class DB:
    """
    New database 
    """
    def __init__(self):
        self.db_name = "pythonaire.db"

    def connect(self):
        """
        Connects to database db_name
        """
        try:
            self.conn = sqlite3.connect(self.db_name)
            # Needs to be added according to ChatGPT 4o
            self.conn.execute("PRAGMA foreign_Keys = ON;")
            self.conn.row_factory = sqlite3.Row
            print(f"\nConnected to {self.db_name}.\n")
            self.cursor = self.conn.cursor()
            return self.conn, self.cursor
        except sqlite3.Error as e:
            print(f"\nFailed to connect to {self.db_name}.\n", e)
            return 0

    def setup(self):
        """
        Creates db and tables
        """
        self.connect()
        self.create_tables(self.db_name)
        self.generate_category_type()
        self.close()

    def create_tables(self, db_name):
        """
        Creates all required tables

        Pending:
        * Check if tables already exist
        """
        if not self.connect():
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
        """
        Loads category types Positive and Negative

        Pending:
        * Check that categories don't already exist
        """
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


class Account(DB):
    """
    Add or list new accounts
    """
    def __init__(self):
        super().__init__()

    def add(self, name, cat_name, notes=""):
        """
        Add a new account
        """

        # Open or create database:
        self.conn, self.cursr = super().connect()

        # Find category.cat_id using cat_name:
        self.cursor.execute("""
           SELECT cat_id FROM category
           WHERE cat_name = (?)
        """, (cat_name,))
        rows = self.cursor.fetchall()
        cat_names = [row[0] for row in rows]
        print(cat_names)


        # Close database:
        super().close()
        


class Category(DB):
    """
    Add or list new categories
    """
    def __init__(self):
        super().__init__()

    def add(self, name, cat_type):
        """
        Add a new category
        """
        data = (name, cat_type)

        # Open or create database:
        self.conn, self.cursor = super().connect()

        # Check if category name already exists:
        self.cursor.execute("""
            SELECT cat_name from category
        """)
        rows = self.cursor.fetchall()
        cat_names = [row[0] for row in rows]
        if name in cat_names:
            print(f"Category {name} already exists, pick a new name.")
        else:
            # Add new category:
            self.cursor.execute("""
                INSERT INTO category (cat_name, type_id)
                VALUES (?,?)
            """, data)
            self.conn.commit()
            print(f"Category {name} added.")

        # Close database:
        super().close()

    def list(self):
        """
        List all the available categories
        """
        # Connect to db:
        self.conn, self.cursor = super().connect()

        # Execute query:
        self.cursor.execute("""
            SELECT category.cat_id, category.cat_name, category_type.cat_type
            FROM category
            JOIN category_type ON category.type_id = category_type.cat_type_id
        """)
        rows = self.cursor.fetchall()
        self.cat = [dict(row) for row in rows]

        # List all the categories
        print("The categories available are:")
        for x in self.cat:
            print(f"ID: {x['cat_id']}\tName: {x['cat_name']}\tType: {x['cat_type']}.")
            #print(x)

        # Close db:
        super().close()
        
if __name__ == "__main__":
    import api 

    cat_name = "Credit"
    cat_type = 2

    acc_name = "Amex"

    # Setup:
    #db = DB()
    #db.setup()

    # Add category:
    cat = Category()
    #cat.add(cat_name, cat_type)

    # List all categories:
    cat.list()

    # Add account:
    acc = Account()
    acc.add(acc_name, cat_name)

    # Delete database
    if 0:
        import os
        db_name = "pythonaire.db"
        file_name = db_name
        if os.path.isfile(file_name):
            os.remove(file_name)
            print(f"{file_name} has been deleted.")
        else:
            print(f"{file_name} does not exist.")

    #self.cursor.execute("""
    #        SELECT * from category_type
    #    """)
    #    rows = self.cursor.fetchall()
    #    categories = [dict(row) for row in rows]
    #    for x in categories:
    #        print(x)
     
