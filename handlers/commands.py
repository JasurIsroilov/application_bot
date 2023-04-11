from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from keyboards import CallbackKb
from .msg import CrewMsg


async def cmd_start(message: types.Message):
    await message.answer(text=CrewMsg.main_menu, reply_markup=CallbackKb.main_menu())


def register_commands(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands='start', chat_type=types.ChatType.PRIVATE)
