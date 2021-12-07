import asyncio
import asyncpg

from loguru import logger


class Database:

    def __init__(self, name: str, user: str, password: str, host: str, port: str, loop: asyncio.AbstractEventLoop) -> None:
        self.pool = loop.run_until_complete(
            asyncpg.create_pool(
                database=name,
                user=user,
                password=password,
                host=host,
                port=port
            )
        )

    async def create_database(self) -> None:
        with open("app/db/init.sql", "r") as f:
            sql = f.read()
        await self.pool.execute(sql)

    async def close_database(self) -> None:
        await self.pool.close()

    async def add_user(self, user_id: int, user_lang: str) -> None:
        await self.pool.execute(f"INSERT INTO Users VALUES({user_id}, '{user_lang}')")
        logger.info(f"New user - user_id: {user_id}; language: {user_lang}")

    async def verification(self, user_id: int) -> bool:
        response = await self.pool.fetchrow(f"SELECT user_id FROM Users WHERE user_id={user_id}")
        return True if response else False

    async def add_order(self, user_id: int, name: str, category: str, short_description: str, price: str, address: str) -> None:
        await self.pool.execute(
            '''
            INSERT INTO Orders(user_id, name, category, short_description, price, address)
            VALUES($1, $2, $3, $4, $5, $6)
            ''', user_id, name, category, short_description, price, address)
        logger.info(f"New order - user_id: {user_id}; order name: {name}")
