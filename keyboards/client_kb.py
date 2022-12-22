from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

btnTopUp = InlineKeyboardButton(text='Пополнить баланс', callback_data="top_up")
topUpMenu = InlineKeyboardMarkup(row_width=1)
topUpMenu.insert(btnTopUp)



def buy_menu(isUrl=True, url="", bill=""):
    qiwiMenu = InlineKeyboardMarkup(row_width=1)
    if isUrl:
        btnUrlQIWI = InlineKeyboardButton(text="Ссылка на оплату", url=url)
        qiwiMenu.insert(btnUrlQIWI)

    btnChecjQIWI = InlineKeyboardButton(text="Проверка оплаты", callback_data='check_'+bill)
    qiwiMenu.insert(btnChecjQIWI)
    return qiwiMenu
