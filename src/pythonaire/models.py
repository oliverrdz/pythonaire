import sqlite3

class DB:
    """
    Handles SQLite database connection, setup, and table creation.
    """

    def __init__(self, db_name="pythonaire.db"):
        self.db_name = db_name

    def connect(self):
        """Connect to SQLite database and return connection and cursor."""
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.conn.execute("PRAGMA foreign_keys = ON;")
            self.conn.row_factory = sqlite3.Row
            self.cursor = self.conn.cursor()
            return self.conn, self.cursor
        except sqlite3.Error as e:
            print(f"\nFailed to connect to {self.db_name}.\n", e)
            return None, None

    def setup(self):
        """Set up database tables and initial data."""
        self.create_tables()
        self.generate_category_type()
        self.close()

    def create_tables(self):
        """Create necessary tables in the database."""
        conn, cursor = self.connect()
        if not conn:
            print(f"\nCan't connect to database {self.db_name}\n")
            return

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS category_type (
                cat_type_id INTEGER PRIMARY KEY AUTOINCREMENT,
                cat_type TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS category (
                cat_id INTEGER PRIMARY KEY AUTOINCREMENT,
                cat_name TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
                acc_id INTEGER PRIMARY KEY AUTOINCREMENT,
                acc_name TEXT NOT NULL,
                cat_id INTEGER NOT NULL,
                acc_total REAL NOT NULL,
                acc_notes TEXT,
                FOREIGN KEY (cat_id) REFERENCES category(cat_id) ON DELETE CASCADE
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                trans_id INTEGER PRIMARY KEY AUTOINCREMENT,
                trans_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                acc_id INTEGER NOT NULL,
                trans_amount REAL NOT NULL,
                cat_type_id INTEGER NOT NULL,
                trans_notes TEXT,
                FOREIGN KEY (acc_id) REFERENCES accounts(acc_id) ON DELETE CASCADE,
                FOREIGN KEY (cat_type_id) REFERENCES category_type(cat_type_id) ON DELETE CASCADE
            )
        """)

        conn.commit()

    def generate_category_type(self):
        """Insert default category types into the database if not already present."""
        self.cursor.execute("SELECT COUNT(*) as count FROM category_type")
        if self.cursor.fetchone()["count"] == 0:
            category_types = [("Expense",), ("Income",)]
            self.cursor.executemany("""
                INSERT INTO category_type (cat_type)
                VALUES (?)""", category_types)
            self.conn.commit()

    def close(self):
        """Close the database connection."""
        if hasattr(self, "conn"):
            self.conn.close()


class BaseModel(DB):
    """
    Base model providing add and list functionality for inheriting classes.
    """
    def __init__(self):
        super().__init__()

    def add(self, data):
        """Insert data using the provided insert_query."""
        self.conn, self.cursor = super().connect()
        self.cursor.execute(self.insert_query, data)
        self.conn.commit()
        print(f"{self.__class__.__name__} entry added.")

    def delete(self, data):
        """Delete entry using the provided delete_query."""
        self.conn, self.cursor = super().connect()
        self.cursor.execute(self.delete_query, data)
        self.conn.commit()
        print(f"{self.__class__.__name__} entry deleted.")

    def list(self):
        """List entries using the provided list_query."""
        self.conn, self.cursor = super().connect()
        self.cursor.execute(self.list_query)
        rows = self.cursor.fetchall()
        self.list_printer(rows)
        super().close()


class Category(BaseModel):
    """
    Manage categories in the database.
    """
    def __init__(self):
        super().__init__()
        self.insert_query = "INSERT INTO category (cat_name) VALUES (?)"
        self.list_query = "SELECT cat_id, cat_name FROM category"
        self.delete_query = "DELETE FROM category WHERE cat_name = ?"

    def add(self, name):
        """Add a category if it does not already exist."""
        self.conn, self.cursor = super().connect()
        self.cursor.execute("SELECT cat_name FROM category")
        if name in [row[0] for row in self.cursor.fetchall()]:
            print(f"Category {name} already exists.")
        else:
            super().add((name,))
        super().close()

    def delete(self, name):
        """Delete a category if it exists."""
        self.conn, self.cursor = super().connect()
        self.cursor.execute("SELECT cat_name FROM category") 
        if name in [row[0] for row in self.cursor.fetchall()]:
            super().delete((name,))
        else:
            print(f"Category {name} does not exist.")
        super().close()

    def list_printer(self, rows):
        """Print category list from fetched rows."""
        print("\nAvailable categories:")
        for row in rows:
            print(f"ID: {row['cat_id']}\tName: {row['cat_name']}")


class Account(BaseModel):
    """
    Manage accounts linked to categories.
    """
    def __init__(self):
        super().__init__()
        self.insert_query = "INSERT INTO accounts (acc_name, cat_id, acc_total, acc_notes) VALUES (?, ?, ?, ?)"
        self.list_query = """
            SELECT acc_id, acc_name, category.cat_name, acc_total, acc_notes
            FROM accounts
            JOIN category ON accounts.cat_id = category.cat_id"""

    def add(self, name, cat_name, notes=""):
        """Add a new account with a category name and optional notes."""
        self.conn, self.cursor = super().connect()
        self.cursor.execute("SELECT cat_id FROM category WHERE cat_name = ?", (cat_name,))
        cat = self.cursor.fetchone()
        if not cat:
            print(f"Category {cat_name} does not exist.")
        else:
            self.cursor.execute("SELECT acc_name FROM accounts WHERE acc_name = ?", (name,))
            if self.cursor.fetchone():
                print(f"Account {name} already exists.")
            else:
                super().add((name, cat["cat_id"], 0.0, notes))
        super().close()

    def list_printer(self, rows):
        """Print account list from fetched rows."""
        print("\nAvailable accounts:")
        for row in rows:
            print(f"ID: {row['acc_id']}\tName: {row['acc_name']}\t"
                  f"Category: {row['cat_name']}\tTotal: {row['acc_total']}\tNotes: {row['acc_notes']}")


class Transaction(BaseModel):
    """
    Manage financial transactions and update account balances.
    """
    def __init__(self):
        super().__init__()
        self.insert_query = "INSERT INTO transactions (acc_id, trans_amount, cat_type_id, trans_notes) VALUES (?, ?, ?, ?)"
        self.list_query = """
            SELECT trans_id, trans_date, accounts.acc_name, trans_amount, trans_notes
            FROM transactions
            JOIN accounts ON transactions.acc_id = accounts.acc_id"""

    def add(self, acc_name, trans_amount, cat_type, trans_notes=""):
        """Add a transaction and update the account total accordingly."""
        self.conn, self.cursor = super().connect()

        self.cursor.execute("SELECT acc_id FROM accounts WHERE acc_name = ?", (acc_name,))
        acc = self.cursor.fetchone()
        if not acc:
            print(f"Account {acc_name} does not exist.")
            super().close()
            return

        acc_id = acc["acc_id"]
        trans_amount = abs(trans_amount) if cat_type == "Income" else -abs(trans_amount)

        self.cursor.execute("SELECT cat_type_id FROM category_type WHERE cat_type = ?", (cat_type,))
        cat_row = self.cursor.fetchone()
        if not cat_row:
            print("Invalid category type.")
            super().close()
            return

        cat_type_id = cat_row["cat_type_id"]

        self.cursor.execute("SELECT acc_total FROM accounts WHERE acc_id = ?", (acc_id,))
        last_total = self.cursor.fetchone()["acc_total"]

        self.cursor.execute(self.insert_query, (acc_id, trans_amount, cat_type_id, trans_notes))
        self.cursor.execute("UPDATE accounts SET acc_total = ? WHERE acc_id = ?",
                            (last_total + trans_amount, acc_id))
        self.conn.commit()
        print(f"Transaction added to {acc_name}")
        super().close()

    def list_printer(self, rows):
        """Print transaction list from fetched rows."""
        print("\nAvailable transactions:")
        for row in rows:
            print(f"ID: {row['trans_id']}\tDate: {row['trans_date']}\t"
                  f"Account: {row['acc_name']}\tAmount: {row['trans_amount']}\tNotes: {row['trans_notes']}")

if __name__ == "__main__":
    if 0:
        db = DB()
        db.setup()

    cat = Category()
    #cat.add("Debit")
    cat.add("Credit")
    cat.list()
    cat.delete("Credit")
    cat.list()
