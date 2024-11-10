import sqlite3
conn = sqlite3.connect('human_detection.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM human_count")
rows = cursor.fetchall()
for row in rows:
    print(row)

conn.close()
