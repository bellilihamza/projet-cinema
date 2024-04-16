import sqlite3

# Connect to SQLite database (creates a new database if not exists)
conn = sqlite3.connect('myDB.db')

# Create a cursor object to execute SQL queries
cursor = conn.cursor()


cursor.execute("SELECT * FROM MOVIE")
for i in cursor.fetchall():
    print(i)

conn.close()

print("SQL queries executed successfully.")

