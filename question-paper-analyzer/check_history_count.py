import sqlite3
import os

db_path = 'database.db'
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT count(*) FROM history")
    print(f"History count: {cursor.fetchone()[0]}")
    cursor.execute("SELECT * FROM history LIMIT 1")
    print(f"Sample row: {cursor.fetchone()}")
    conn.close()
else:
    print("Database not found")
