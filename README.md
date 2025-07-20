# Pythonaire

**Pythonaire** is a lightweight command-line personal finance tracker built with Python and SQLite. It allows you to manage categories, accounts, and transactions while keeping your account balances updated automatically.

## Features

- 📂 Create and list categories (e.g., Debit, Credit, Savings)
- 💼 Add and list accounts linked to categories
- 💸 Record income and expenses as transactions
- 🔄 Automatically update account balances based on transactions
- 🗂 Structured with OOP for extendability and clarity

## Getting Started

### Requirements

- Python 3.7+
- SQLite (built-in with Python via `sqlite3`)

### Installation

Clone the repository and run the script:

```bash
git clone https://github.com/yourusername/pythonaire.git
cd pythonaire
pip3 install .
```

You can also install the PyPi build via pip:

```bash
pip3 install pythonaire
```

### Sample Categories

- Debit
- Credit
- Savings

### Sample Accounts

- BBVA (Debit)
- Amex (Credit)
- Monzo (Debit)

### Sample Transactions

- Income and expenses on the above accounts

## How to use
* Pending

## Code Structure

The application follows an object-oriented approach with the following classes:

- `DB`: Handles database connection and schema creation
- `BaseModel`: Abstract class for common add/list methods
- `Category`: Manages financial categories
- `Account`: Manages bank accounts and links to categories
- `Transaction`: Manages income/expense transactions and updates balances

## Development

This project is designed to be modular. It can be extended by:

- Adding a GUI or web interface
- Exporting reports to PDF or CSV

## Author

Oliver Rodriguez  
Powered by ChatGPT  
2025
