# database/db.py
import aiosqlite

async def create_db():
    async with aiosqlite.connect("database.db") as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY,
                user_id INTEGER
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS requests(
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                type TEXT,
                content TEXT
            )
        """)
        await db.commit()