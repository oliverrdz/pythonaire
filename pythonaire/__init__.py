"""
Pythonaire - A Personal Finance Tracker

This package provides classes to manage:
- Categories of financial accounts
- Accounts associated with categories
- Transactions (income/expenses) linked to accounts

SQLite is used as the database backend.
"""

from .database import DB
from .models import Category, Account, Transaction

__all__ = ["DB", "Category", "Account", "Transaction"]
__version__ = "0.1.0"
