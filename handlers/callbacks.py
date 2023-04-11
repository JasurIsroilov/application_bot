from contextlib import suppress

from aiogram import types, Dispatcher
from aiogram.utils.exceptions import MessageNotModified, MessageCantBeEdited, MessageToEditNotFound
from aiogram.dispatcher import FSMContext

from .msg import CrewMsg
from keyboards import CallbackKb
from callback_factory import crew_cb, msg_cb
from config_reader import MsgState, config, bot
from db.models import Crew


async def edit_or_answer(callback: types.CallbackQuery, text: str, markup: types.InlineKeyboardMarkup) -> None:
    with suppress(MessageNotModified):
        try:
            await callback.message.edit_text(text=text, reply_markup=markup)
        except MessageCantBeEdited | MessageToEditNotFound:
            await callback.message.answer(text=text, reply_markup=markup)
    await callback.answer()


async def kill_state(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await callback.message.answer(CrewMsg.main_menu, reply_markup=CallbackKb.main_menu())


async def support_menu(callback: types.CallbackQuery, callback_data) -> None:
    await edit_or_answer(callback=callback, text=CrewMsg.support_menu, markup=CallbackKb.support())
    await callback.answer()


async def support_choose(callback: types.CallbackQuery, callback_data) -> None:
    match callback_data.get('action'):
        case 'task':
            await MsgState.waiting_input.set()
            await edit_or_answer(callback=callback, text=CrewMsg.support_task,
                                 markup=CallbackKb.msg_check(callback_data.get('type')))
        case 'trouble':
            await MsgState.waiting_input.set()
            await edit_or_answer(callback=callback, text=CrewMsg.support_trouble,
                                 markup=CallbackKb.msg_check(callback_data.get('type')))
        case 'back':
            await edit_or_answer(callback=callback, text=CrewMsg.main_menu, markup=CallbackKb.main_menu())


async def hr_menu(callback: types.CallbackQuery, callback_data) -> None:
    await edit_or_answer(callback=callback, text=CrewMsg.hr, markup=CallbackKb.hr())
    await callback.answer()


async def hr_choose(callback: types.CallbackQuery, callback_data):
    match callback_data.get('action'):
        case 'newcomer':
            await MsgState.waiting_input.set()
            await edit_or_answer(callback=callback, text=CrewMsg.hr_newcomer,
                                 markup=CallbackKb.msg_check(c_type=callback_data.get('type')))
        case 'firing':
            await MsgState.waiting_input.set()
            await edit_or_answer(callback=callback, text=CrewMsg.hr_newcomer,
                                 markup=CallbackKb.msg_check(callback_data.get('type')))
        case 'back':
            await edit_or_answer(callback=callback, text=CrewMsg.main_menu, markup=CallbackKb.main_menu())


async def back_to_choice(callback: types.CallbackQuery, callback_data, state: FSMContext):
    await state.finish()
    match callback_data.get('type'):
        case 'support':
            await support_menu(callback, callback_data)
        case 'hr':
            await hr_menu(callback, callback_data)


async def msg_input(message: types.Message, state: FSMContext, user: Crew):
    async with state.proxy() as data:
        data['msg'] = CrewMsg.msg_header.format(
            user.fio, user.phone, user.username, user.dep
        ) + message.text
        await message.answer(data['msg'], reply_markup=CallbackKb.msg_send())


async def msg_send(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data.get('action') == 'send':
        async with state.proxy() as data:
            await callback.message.answer(data['msg'])
            await bot.send_message(chat_id=config.group_id, text=data['msg'])
    elif callback_data.get('action') == 'retry':
        await edit_or_answer(callback=callback, text=CrewMsg.hr, markup=CallbackKb.msg_check('support'))
        await callback.answer()
        return
    await kill_state(callback=callback, state=state)
    await callback.answer()


def register_callbacks(dp: Dispatcher):
    dp.register_callback_query_handler(support_menu, crew_cb.filter(type='support', action='choose'),
                                       chat_type=types.ChatType.PRIVATE)
    dp.register_callback_query_handler(support_choose, crew_cb.filter(type='support'),
                                       chat_type=types.ChatType.PRIVATE)

    dp.register_callback_query_handler(hr_menu, crew_cb.filter(type='hr', action='choose'),
                                       chat_type=types.ChatType.PRIVATE)
    dp.register_callback_query_handler(hr_choose, crew_cb.filter(type='hr'),
                                       chat_type=types.ChatType.PRIVATE)

    dp.register_callback_query_handler(back_to_choice, msg_cb.filter(action='back'), state=MsgState.waiting_input,
                                       chat_type=types.ChatType.PRIVATE)
    dp.register_callback_query_handler(msg_send, msg_cb.filter(type='send'), state=MsgState.waiting_input,
                                       chat_type=types.ChatType.PRIVATE)

    dp.register_message_handler(msg_input, content_types='text', state=MsgState.waiting_input,
                                chat_type=types.ChatType.PRIVATE)
