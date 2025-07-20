import sqlite3

class DB:
    """
    New database 
    """
    def __init__(self, db_name="pythonaire.db"):
        self.db_name = db_name

    def connect(self):
        """
        Connects to database db_name
        """
        try:
            self.conn = sqlite3.connect(self.db_name)
            # Needs to be added according to ChatGPT 4o
            self.conn.execute("PRAGMA foreign_Keys = ON;")
            self.conn.row_factory = sqlite3.Row
            self.cursor = self.conn.cursor()
            return self.conn, self.cursor
        except sqlite3.Error as e:
            print(f"\nFailed to connect to {self.db_name}.\n", e)
            return 0

    def setup(self):
        """
        Creates db and tables
        """
        self.create_tables(self.db_name)
        self.generate_category_type()
        self.close()

    def create_tables(self, db_name):
        """
        Creates all required tables
        """
        if not self.connect():
            print(f"\nCan't connect to database {db_name}\n")
            return 0

        # Create table category_type (e.g. Expense/Income):
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
        cat_name varchar(100))
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
        cat_type_id integer NOT NULL,
        trans_notes text,
        FOREIGN KEY (acc_id) REFERENCES accounts(acc_id),
        FOREIGN KEY (cat_type_id) REFERENCES category_type(cat_type_id)
        )
        """)
        print("Table transactions created\n")

    def generate_category_type(self):
        """
        Loads category types Expense / Income

        Pending:
        * Check that categories don't already exist
        """
        category_types = [
            ("Expense",),
            ("Income",)
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


class Category(DB):
    """
    Add or list new categories
    """
    def __init__(self):
        super().__init__()

    def add(self, name):
        """
        Add a new category
        """
        data = (name,)

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
                INSERT INTO category (cat_name)
                VALUES (?)
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
            SELECT category.cat_id, category.cat_name
            FROM category
        """)
        rows = self.cursor.fetchall()
        self.cat = [dict(row) for row in rows]

        # List all the categories
        print("\nThe categories available are:")
        for x in self.cat:
            print(f"ID: {x['cat_id']}\tName: {x['cat_name']}.")
        print("")
        # Close db:
        super().close()


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
        existing_category = 0
        self.cursor.execute("""
           SELECT cat_id FROM category
           WHERE cat_name = (?)
        """, (cat_name,))
        rows = self.cursor.fetchall()
        try:
            cat_id = rows[0][0]
        except:
            print(f"Category {cat_name} does not exist. Try again.")
            return 0

        # Check if account already exists:
        existing_account = 0
        self.cursor.execute("""
            SELECT acc_name from accounts
            WHERE acc_name = (?)
        """, (name,)) 
        rows = self.cursor.fetchall()
        try:
            existing_account = rows[0][0]
            print(f"Account {name} already exists. Try again.")
        except:
            pass

        # Add account:
        if cat_id != 0 and existing_account == 0:
            data = (name, cat_id, 0, notes)
            self.cursor.execute("""
                INSERT INTO accounts (acc_name, cat_id, acc_total, acc_notes)
                VALUES (?,?,?,?)
            """, data)
            self.conn.commit()
            print(f"Account {name} added.")

        # Close database:
        super().close()

    def list(self):
        """
        List all available accounts
        """
        # Connect to db:
        self.conn, self.cursor = super().connect()

        # Execute query:
        self.cursor.execute("""
            SELECT accounts.acc_id, accounts.acc_name, category.cat_name, 
            accounts.acc_total, accounts.acc_notes
            FROM accounts
            JOIN category ON accounts.cat_id = category.cat_id
        """)
        rows = self.cursor.fetchall()
        acc = [dict(row) for row in rows]

        # List all the accounts
        print("\nThe available accounts are:")
        for x in acc:
            message = (
            f"ID: {x['acc_id']}\tName: {x['acc_name']}\t"
            f"Category: {x['cat_name']}\tTotal: {x['acc_total']}\t"
            f"Notes: {x['acc_notes']}"
            )
            print(message)
        print("")
        # Close db:
        super().close()


class Transaction(DB):
    """
    Add or list all transactions
    """
    def __init__(self):
        super().__init__()

    def add(self, acc_name, trans_amount, cat_type, trans_notes=""):
        """
        Add a new transaction
        """

        # Open or create database:
        self.conn, self.cursor = super().connect()

        # Find account with name acc_name:
        self.cursor.execute("""
            SELECT a.acc_name, a.acc_id
            FROM accounts a
            WHERE a.acc_name = ?
        """, (acc_name,))
        rows = self.cursor.fetchall()
        data = [dict(row) for row in rows]
        if data:
            acc_id = data[0]["acc_id"]
        else:
            print(f"Account {acc_name} does not exist. Try again.")
            return 0

        # Check if the amount added is either Income or Expense:
        if cat_type == "Income":
            # Ensure amount added is always positive:
            trans_amount = abs(trans_amount)
        elif cat_type == "Expense":
            # Ensure amount added is always negative:
            trans_amount = -abs(trans_amount)
        else:
            print("Type of transaction incorrect. Please select Income or Expense.")
            return 0

        # Find cat_type_id from category_type table:
        self.cursor.execute("""
            SELECT cat_type_id FROM category_type
            WHERE  cat_type= ?
        """, (cat_type,))
        cat_type_id = self.cursor.fetchall()[0][0]

       # Find last amount from selected account:
        self.cursor.execute("""
            SELECT acc_total, acc_name FROM accounts
            WHERE acc_name = ?
        """, (acc_name,))
        last_amount, acc_name = self.cursor.fetchall()[0]

        # Add new transaction:
        data = (acc_id, trans_amount, cat_type_id, trans_notes) 
        self.cursor.execute("""
            INSERT INTO transactions (acc_id, trans_amount, 
            cat_type_id, trans_notes)
            VALUES (?,?,?,?)
        """, data) 
        self.cursor.execute("""
            UPDATE accounts
            SET acc_total = ?
            WHERE acc_id = ?
        """, (trans_amount + last_amount, acc_id))
        self.conn.commit()
        print(f"Added {trans_amount} to account {acc_name}")
        
    def list(self):
        """
        List all transactions
        """
        # Connect to db:
        self.conn, self.cursor = super().connect()

        # Execute query:
        self.cursor.execute("""
        SELECT t.trans_id, t.trans_date, accounts.acc_name, 
        t.trans_amount, t.trans_notes
        FROM transactions t
        JOIN accounts ON t.acc_id = accounts.acc_id
        """)
        rows = self.cursor.fetchall()
        trans = [dict(row) for row in rows]

        # List all transactions:
        print("\nThe available transactions are:")
        for x in trans:
            message = (
            f"ID: {x['trans_id']}\tDate: {x['trans_date']}\t"
            f"Account: {x['acc_name']}\tAmount: {x['trans_amount']}\t"
            f"Notes: {x['trans_notes']}"
            )
            print(message)

        # Close db:
        super().close()

        

if __name__ == "__main__":

    # Create DB:
    db = DB()
    db.setup()
    
    # Create category:
    cat = Category()
    cat.add(name="Debit")
    cat.add(name="Credit")
    cat.add(name="Savings")
    cat.list()

    # Create account:
    acc = Account()
    acc.add(name="BBVA", cat_name="Debit", notes="")
    acc.add(name="Amex", cat_name="Credit", notes="")
    acc.add("Monzo", "Debit")
    acc.list()
   
    # Create transaction:
    trans = Transaction()
    trans.add(acc_name="BBVA", trans_amount=50, cat_type="Income", trans_notes="")
    trans.add("BBVA", 100, "Income")
    trans.add("Amex", 100, "Expense")
    trans.add("Amex", 50, "Income")
    trans.add("BBVA", 50, "Expense")
    trans.list()

    acc.list()
    

