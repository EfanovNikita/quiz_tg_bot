import aiosqlite

DB_NAME = 'quiz_bot.db'

async def create_table():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS quiz_state (user_id INTEGER PRIMARY KEY, question_index INTEGER, points INTEGER)''')
        await db.commit()

async def update_quiz_index_and_points(user_id, index, points):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('INSERT OR REPLACE INTO quiz_state (user_id, question_index, points) VALUES (?, ?, ?)', (user_id, index, points))
        await db.commit()

async def get_quiz_index(user_id):
     async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT question_index FROM quiz_state WHERE user_id = (?)', (user_id, )) as cursor:
            results = await cursor.fetchone()
            if results is not None:
                return results[0]
            else:
                return 0

async def get_points(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT points FROM quiz_state WHERE user_id = (?)', (user_id, )) as cursor:
            results = await cursor.fetchone()
            if results is not None:
                return results[0]
            else:
                return 0
            
async def get_all():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT user_id, points FROM quiz_state ORDER BY points desc LIMIT 5') as cursor:
            results = await cursor.fetchall()
            return results