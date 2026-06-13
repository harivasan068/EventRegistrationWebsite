import sqlite3

conn = sqlite3.connect('database.db')

cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS events(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    description TEXT,
    date TEXT,
    venue TEXT
)
''')

conn.commit()
conn.close()

print("Database Created Successfully")