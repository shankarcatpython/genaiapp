import sqlite3

# Connect to the database
conn = sqlite3.connect('../../../genieai.db')

# Query to retrieve all table names
tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()

# Print all table names
print("Tables in the database:")
for table in tables:
    print(table[0])

# Close the connection
conn.close()
