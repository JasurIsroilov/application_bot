from pydantic import BaseSettings, SecretStr, PostgresDsn, Field

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup


class MsgState(StatesGroup):
    waiting_input = State()


class Settings(BaseSettings):
    """
    The class handling secret datas
    """
    bot_token: SecretStr
    db_url: PostgresDsn
    group_id: str = Field(env='GROUP_ID')

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


config = Settings()

# configure bot
bot = Bot(config.bot_token.get_secret_value(), parse_mode='HTML')
# configure dispatcher
dp = Dispatcher(bot=bot, storage=MemoryStorage())
