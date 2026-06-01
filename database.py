import aiosqlite
import os

DB_PATH = "data/stories.db"


async def init_db():
    os.makedirs("data", exist_ok=True)

    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS stories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            content TEXT
        )
        """)

        await db.execute("""
        CREATE TABLE IF NOT EXISTS ratings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            story_id INTEGER,
            user_id INTEGER,
            rating INTEGER
        )
        """)

        await db.commit()


async def add_story(title, content):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO stories (title, content) VALUES (?, ?)",
            (title, content)
        )
        await db.commit()


async def get_stories():
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute("SELECT id, title FROM stories")
        return await cur.fetchall()


async def get_story(story_id):
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(
            "SELECT * FROM stories WHERE id=?",
            (story_id,)
        )
        return await cur.fetchone()


async def delete_story(story_id):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("DELETE FROM stories WHERE id=?", (story_id,))
        await db.commit()


async def add_rating(story_id, user_id, rating):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "DELETE FROM ratings WHERE story_id=? AND user_id=?",
            (story_id, user_id)
        )

        await db.execute(
            "INSERT INTO ratings (story_id, user_id, rating) VALUES (?, ?, ?)",
            (story_id, user_id, rating)
        )

        await db.commit()


async def get_rating(story_id):
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(
            "SELECT AVG(rating), COUNT(*) FROM ratings WHERE story_id=?",
            (story_id,)
        )
        return await cur.fetchone()

async def update_story(story_id, content):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE stories SET content=? WHERE id=?",
            (content, story_id)
        )
        await db.commit()