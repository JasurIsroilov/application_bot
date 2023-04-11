from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.handler import CancelHandler
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy import select


from db import Crew


class ValidatorMiddleware(BaseMiddleware):
    """
    Checks user from the database and returns session connection to
    handler as session
    """
    def __init__(self, session_pool: async_sessionmaker):
        super().__init__()
        self.session_pool = session_pool

    async def on_process_message(self,
                                 event: types.Message,
                                 data: dict):
        async with self.session_pool() as session:
            slct = select(Crew).where(Crew.username == event.from_user.username)
            query = await session.execute(slct)
            query = query.fetchone()
            if not query:
                await event.answer('Вас нет в БД!')
                raise CancelHandler()
        for q in query:
            data['user'] = q
            break

    async def on_process_callback_query(self,
                                        event: types.CallbackQuery,
                                        data: dict):
        async with self.session_pool() as session:
            slct = select(Crew).where(Crew.username == event.from_user.username)
            query = await session.execute(slct)
            query = query.fetchone()
            if not query:
                await event.message.answer('Вас нет в БД!')
                raise CancelHandler()
            for q in query:
                data['user'] = q
                break
