import sqlite3

# Step 1: Connect to SQLite database (it will create the database file if it doesn't exist)
conn = sqlite3.connect('human_detection.db')

# Step 2: Create a cursor object to interact with the database
cursor = conn.cursor()

# Step 3: Create a table for storing human count data if it doesn't already exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS human_count (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        count INTEGER,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')

# Step 4: Create a table for storing total human count for 2-minute intervals
cursor.execute('''
    CREATE TABLE IF NOT EXISTS total_count (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        total_count INTEGER,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')


# Step 5: Commit the changes and close the connection
conn.commit()
conn.close()

print("Database and tables created successfully.")
