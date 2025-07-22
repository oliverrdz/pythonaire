import pythonaire as pa

# Generate DB:
db = pa.DB()
db.setup()

# Add categories:
cat = pa.models.Category()
cat.add("Debit")
cat.add("Credit")
cat.add("Investments")
cat.add("Retirement")
cat.list()

# Add accounts:
acc = pa.models.Account()
acc.add("BoA", "Debit")
acc.add("Chase", "Debit")
acc.add("Discover", "Credit")
acc.list()

# Add transactions:
trans = pa.models.Transaction()
trans.add("Chase", 50, "Income", "Rebate")
trans.add("Discover", 100, "Expense", "Groceries")
trans.add("BoA", 1000, "Income", "Salary")
trans.list()
