import sqlite3

# Connect to the database
conn = sqlite3.connect('my_database.db')

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

# Execute a SELECT query to retrieve all rows from a table
cursor.execute('SELECT * FROM data')

# Fetch all rows and print them to the console
rows = cursor.fetchall()
for row in rows:
    print(row)

# Close the cursor and connection
cursor.close()
conn.close()
