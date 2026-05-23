import aiosqlite

DB_NAME = "stories.db"

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS stories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                text TEXT,
                image TEXT
            )
        """)
        await db.commit()

async def add_story(title, text, image):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT INTO stories (title, text, image) VALUES (?, ?, ?)",
            (title, text, image)
        )
        await db.commit()

async def get_stories():
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT * FROM stories")
        return await cursor.fetchall()

async def get_story(story_id):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            "SELECT * FROM stories WHERE id = ?",
            (story_id,)
        )
        return await cursor.fetchone()