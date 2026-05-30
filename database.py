import sqlite3

db = sqlite3.connect("data/stories.db")
cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS stories(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    content TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS ratings(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    story_id INTEGER,
    user_id INTEGER,
    rating INTEGER
)
""")

db.commit()