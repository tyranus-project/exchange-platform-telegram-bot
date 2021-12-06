import asyncio
import asyncpg


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
