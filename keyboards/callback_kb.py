from aiogram import types

from callback_factory import crew_cb, msg_cb


class CallbackKb:
    """
    The set of callback keyboards
    """
    @staticmethod
    def main_menu() -> types.InlineKeyboardMarkup:
        markup = types.InlineKeyboardMarkup(row_width=3)
        markup.row(
            types.InlineKeyboardMarkup(text='Тех. поддержка',
                                       callback_data=crew_cb.new(type='support', action='choose'))
        )
        markup.row(
            types.InlineKeyboardMarkup(text='HR',
                                       callback_data=crew_cb.new(type='hr', action='choose')))
        return markup

    @staticmethod
    def support() -> types.InlineKeyboardMarkup:
        markup = types.InlineKeyboardMarkup(row_width=3)
        markup.row(
            types.InlineKeyboardMarkup(text='Задача',
                                       callback_data=crew_cb.new(type='support', action='task'))
        )
        markup.row(
            types.InlineKeyboardMarkup(text='Проблема',
                                       callback_data=crew_cb.new(type='support', action='trouble')))
        markup.row(
            types.InlineKeyboardMarkup(text='Назад',
                                       callback_data=crew_cb.new(type='support', action='back')))
        return markup

    @staticmethod
    def hr() -> types.InlineKeyboardMarkup:
        markup = types.InlineKeyboardMarkup(row_width=3)
        markup.row(
            types.InlineKeyboardMarkup(text='Выход сотрудника',
                                       callback_data=crew_cb.new(type='hr', action='newcomer'))
        )
        markup.row(
            types.InlineKeyboardMarkup(text='Уход сотрудника',
                                       callback_data=crew_cb.new(type='hr', action='firing'))
        )
        markup.row(
            types.InlineKeyboardMarkup(text='Назад',
                                       callback_data=crew_cb.new(type='hr', action='back'))
        )
        return markup

    @staticmethod
    def msg_check(c_type: str) -> types.InlineKeyboardMarkup:
        markup = types.InlineKeyboardMarkup(row_width=3)
        markup.row(
            types.InlineKeyboardMarkup(
                text='Назад',
                callback_data=msg_cb.new(type=c_type, action='back')
            )
        )
        return markup

    @staticmethod
    def msg_send() -> types.InlineKeyboardMarkup:
        markup = types.InlineKeyboardMarkup(row_width=3)
        markup.row(
            types.InlineKeyboardMarkup(
                text='Отправить',
                callback_data=msg_cb.new(type='send', action='send')
            )
        )
        markup.row(
            types.InlineKeyboardMarkup(
                text='Редактировать',
                callback_data=msg_cb.new(type='send', action='retry')
            )
        )
        markup.row(
            types.InlineKeyboardMarkup(
                text='Главное меню',
                callback_data=msg_cb.new(type='send', action='main_menu')
            )
        )
        return markup
