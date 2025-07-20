import unittest
import os
from api import DB, Category, Account, Transaction

class TestDatabaseFunctions(unittest.TestCase):
    """
    Unit tests for database operations involving Category, Account, and Transaction classes.
    Uses a temporary SQLite test database to validate functionality.
    """

    def setUp(self):
        """Set up a fresh test database before each test."""
        self.test_db = "test_pythonaire.db"
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
        self.db = DB(db_name=self.test_db)
        self.db.setup()
        self.cat = Category()
        self.cat.db_name = self.test_db
        self.acc = Account()
        self.acc.db_name = self.test_db
        self.trans = Transaction()
        self.trans.db_name = self.test_db

    def test_add_category(self):
        """Test that a category can be successfully added."""
        self.cat.add("TestCat")
        self.cat.conn, self.cat.cursor = self.cat.connect()
        self.cat.cursor.execute("SELECT * FROM category WHERE cat_name = ?", ("TestCat",))
        result = self.cat.cursor.fetchone()
        self.assertIsNotNone(result)
        self.cat.close()

    def test_add_account(self):
        """Test that an account can be successfully added to a category."""
        self.cat.add("Checking")
        self.acc.add("TestAcc", "Checking")
        self.acc.conn, self.acc.cursor = self.acc.connect()
        self.acc.cursor.execute("SELECT * FROM accounts WHERE acc_name = ?", ("TestAcc",))
        result = self.acc.cursor.fetchone()
        self.assertIsNotNone(result)
        self.acc.close()

    def test_add_transaction(self):
        """Test that a transaction is correctly recorded and linked to an account."""
        self.cat.add("Savings")
        self.acc.add("Bank", "Savings")
        self.trans.add("Bank", 200, "Income", "Initial deposit")
        self.trans.conn, self.trans.cursor = self.trans.connect()
        self.trans.cursor.execute("SELECT * FROM transactions WHERE trans_amount = ?", (200,))
        result = self.trans.cursor.fetchone()
        self.assertIsNotNone(result)
        self.trans.close()

    def tearDown(self):
        """Remove the test database after each test run."""
        if os.path.exists(self.test_db):
            os.remove(self.test_db)


if __name__ == "__main__":
    unittest.main()