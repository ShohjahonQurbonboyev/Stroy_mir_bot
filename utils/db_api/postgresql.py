from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config


class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME,
        )

    async def execute(
        self,
        command,
        *args,
        fetch: bool = False,
        fetchval: bool = False,
        fetchrow: bool = False,
        execute: bool = False,
    ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        surname VARCHAR(255) NOT NULL,
        phone_number VARCHAR(255) NOT NULL,
        photo VARCHAR(255) NOT NULL,
        username varchar(255) NULL,
        account VARCHAR(255) NOT NULL,
        telegram_id BIGINT NOT NULL UNIQUE
        );
        """
        await self.execute(sql, execute=True)



    async def create_table_fake_user(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Fake (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        surname VARCHAR(255) NOT NULL,
        phone_number VARCHAR(255) NOT NULL,
        photo VARCHAR(255) NOT NULL,
        username varchar(255) NULL,
        telegram_id BIGINT NOT NULL UNIQUE
        );
        """
        await self.execute(sql, execute=True)



    async def create_table_cod(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Code (
        id SERIAL PRIMARY KEY,
        code VARCHAR(255) NOT NULL UNIQUE,
        point VARCHAR(255) NOT NULL,
        used BOOLEAN DEFAULT False
        );
        """
        await self.execute(sql, execute=True)


    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join(
            [f"{item} = ${num}" for num, item in enumerate(parameters.keys(), start=1)]
        )
        return sql, tuple(parameters.values())

    async def add_user(self, name, surname, phone_number, photo, username, account, telegram_id):
        sql = "INSERT INTO users (name, surname, phone_number, photo, username, account, telegram_id) VALUES($1, $2, $3, $4, $5, $6, $7) returning *"
        return await self.execute(sql, name, surname, phone_number, photo, username, account, telegram_id, fetchrow=True)
    
    async def add_fake(self, name, surname, phone_number, photo, username, telegram_id):
        sql = "INSERT INTO Fake (name, surname, phone_number, photo, username, telegram_id) VALUES($1, $2, $3, $4, $5, $6) returning *"
        return await self.execute(sql, name, surname, phone_number, photo, username, telegram_id, fetchrow=True)

    async def add_code(self, code, point, used):
        sql = "INSERT INTO Code (code, point, used) VALUES($1, $2, $3) returning *"
        return await self.execute(sql, code, point, used, fetchrow=True)


    async def select_all_users(self):
        sql = "SELECT * FROM Users"
        return await self.execute(sql, fetch=True)
    
    async def select_all_faker(self):
        sql = "SELECT * FROM Fake"
        return await self.execute(sql, fetch=True)
    
    async def select_all_code(self):
        sql = "SELECT * FROM Code"
        return await self.execute(sql, fetch=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)
    
    async def select_fake(self, **kwargs):
        sql = "SELECT * FROM Fake WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)
    
    async def select_code(self, **kwargs):
        sql = "SELECT * FROM Code WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)
    

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM Users"
        return await self.execute(sql, fetchval=True)
    
    async def count_code(self):
        sql = "SELECT COUNT(*) FROM Code"
        return await self.execute(sql, fetchval=True)

    async def update_user_username(self, username, telegram_id):
        sql = "UPDATE Users SET username=$1 WHERE telegram_id=$2"
        return await self.execute(sql, username, telegram_id, execute=True)
    
    async def update_user_acoount(self, account, telegram_id):
        sql = "UPDATE Users SET account=$1 WHERE telegram_id=$2"
        return await self.execute(sql, account, telegram_id, execute=True)
    
    async def update_code(self, used, code):
        sql = "UPDATE code SET used=$1 WHERE code=$2"
        return await self.execute(sql, used, code, execute=True)

    async def delete_users(self):
        await self.execute("DELETE FROM Users WHERE TRUE", execute=True)

    async def delete_codes(self):
        await self.execute("DELETE FROM Code WHERE TRUE", execute=True)

    async def delete_user(self, telegram_id):
    # Berilgan Telegram ID bo'yicha foydalanuvchini o'chirish
        sql = "DELETE FROM Users WHERE telegram_id=$1"
        return await self.execute(sql, telegram_id, execute=True)
    
    async def delete_fake(self, telegram_id):
    # Berilgan Telegram ID bo'yicha foydalanuvchini o'chirish
        sql = "DELETE FROM Fake WHERE telegram_id=$1"
        return await self.execute(sql, telegram_id, execute=True)
    
    async def delete_code(self, code):
        sql = "DELETE FROM Code WHERE code=$2"
        return await self.execute(sql, code, execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE Users", execute=True)
