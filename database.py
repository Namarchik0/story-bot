import aiosqlite


async def create_db():

    async with aiosqlite.connect("stories.db") as db:

        await db.execute("""
        CREATE TABLE IF NOT EXISTS stories(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            text TEXT,
            photo TEXT
        )
        """)

        await db.commit()


async def add_story(title, text, photo):

    async with aiosqlite.connect("stories.db") as db:

        await db.execute(
            """
            INSERT INTO stories(title, text, photo)
            VALUES(?,?,?)
            """,
            (title, text, photo)
        )

        await db.commit()


async def get_stories():

    async with aiosqlite.connect("stories.db") as db:

        cursor = await db.execute(
            "SELECT * FROM stories"
        )

        return await cursor.fetchall()


async def get_story(story_id):

    async with aiosqlite.connect("stories.db") as db:

        cursor = await db.execute(
            "SELECT * FROM stories WHERE id=?",
            (story_id,)
        )

        return await cursor.fetchone()