import asyncio

from db_conf import sessionmaker, engine
from updates_configure import get_handled_updates_list
from handlers import register_commands, register_callbacks
from middlewares import ValidatorMiddleware
from db import Base
from config_reader import dp


async def init_models():
    # Create all tables if not exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def app():
    dp.middleware.setup(ValidatorMiddleware(session_pool=sessionmaker))
    register_commands(dp)
    register_callbacks(dp)

    # start bot, then close bot with closing all connections
    try:
        await dp.start_polling(allowed_updates=get_handled_updates_list(dp))
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()


async def starter():
    await init_models()
    await app()


if __name__ == '__main__':
    asyncio.run(starter())
