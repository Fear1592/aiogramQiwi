from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

btnBanned = InlineKeyboardButton(text='ЗАБЛОКИРОВАТЬ', callback_data="banned")
topBanned = InlineKeyboardMarkup(row_width=1)
topBanned.insert(btnBanned)

btnUnBanned = InlineKeyboardButton(text='РАЗБЛОКИРОВАТЬ', callback_data="unbanned")
topUnBanned = InlineKeyboardMarkup(row_width=1)
topUnBanned.insert(btnUnBanned)




def get_keyboard():
    buttons = [
        InlineKeyboardButton(text="Список пользователей, баланс", callback_data="all_balance"),
        InlineKeyboardButton(text="Изминение баланса пользователя", callback_data="update_balance"),
        InlineKeyboardButton(text="Блокировка пользователя", callback_data="block_user"),
        InlineKeyboardButton(text="Выгрузка логов", callback_data="show_logs")
    ]
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard


def get_keyboard_logs():
    buttons = [
        InlineKeyboardButton(text="Выгрузка DEBUG , INFO логов", callback_data="debug_logs"),
        InlineKeyboardButton(text="Выгрузка WARNING логов", callback_data="warning_logs"),
    ]
    keyboard_logs = InlineKeyboardMarkup(row_width=1)
    keyboard_logs.add(*buttons)
    return keyboard_logs
