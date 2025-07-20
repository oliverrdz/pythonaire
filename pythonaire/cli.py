import argparse
from pythonaire.database import DB
from pythonaire.models import Category, Account, Transaction

def init_db():
    db = DB()
    db.setup()
    print("Database initialized.")

def add_category(args):
    Category().add(args.name)

def list_categories(_):
    Category().list()

def add_account(args):
    Account().add(args.name, args.category, args.notes)

def list_accounts(_):
    Account().list()

def add_transaction(args):
    Transaction().add(args.account, args.amount, args.type, args.notes)

def list_transactions(_):
    Transaction().list()

def main():
    parser = argparse.ArgumentParser(description="Pythonaire CLI - Personal Finance Tracker")

    subparsers = parser.add_subparsers(dest='command')
    subparsers.required = True

    # Initialize DB
    init_parser = subparsers.add_parser('init', help='Initialize the database')
    init_parser.set_defaults(func=lambda args: init_db())

    # Category
    cat_add = subparsers.add_parser('add-category', help='Add a new category')
    cat_add.add_argument('name', help='Category name')
    cat_add.set_defaults(func=add_category)

    cat_list = subparsers.add_parser('list-categories', help='List all categories')
    cat_list.set_defaults(func=list_categories)

    # Account
    acc_add = subparsers.add_parser('add-account', help='Add a new account')
    acc_add.add_argument('name', help='Account name')
    acc_add.add_argument('category', help='Category name (must exist)')
    acc_add.add_argument('--notes', default="", help='Optional notes')
    acc_add.set_defaults(func=add_account)

    acc_list = subparsers.add_parser('list-accounts', help='List all accounts')
    acc_list.set_defaults(func=list_accounts)

    # Transaction
    trans_add = subparsers.add_parser('add-transaction', help='Add a new transaction')
    trans_add.add_argument('account', help='Account name')
    trans_add.add_argument('amount', type=float, help='Transaction amount')
    trans_add.add_argument('type', choices=['Income', 'Expense'], help='Transaction type')
    trans_add.add_argument('--notes', default="", help='Optional notes')
    trans_add.set_defaults(func=add_transaction)

    trans_list = subparsers.add_parser('list-transactions', help='List all transactions')
    trans_list.set_defaults(func=list_transactions)

    # Parse and dispatch
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
