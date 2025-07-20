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
                FOREIGN KEY (cat_id) REFERENCES category(cat_id)
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
                FOREIGN KEY (acc_id) REFERENCES accounts(acc_id),
                FOREIGN KEY (cat_type_id) REFERENCES category_type(cat_type_id)
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
