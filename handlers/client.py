from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import dp, bot, db, p2p, logger, cfg
import keyboards.client_kb as nav
import random

class dialog(StatesGroup):
    command = State()


def is_number(_str):
    try:
        int(_str)
        return True
    except ValueError:
        return False


@logger.catch
async def send_sticker_id(message: types.Message):
    if message.chat.type == 'private':
        if not db.user_exsist(message.from_user.username):
            db.add_user(message.from_user.id, message.from_user.username)
            if not db.check_ban_user(message.from_user.username):
                logger.debug(f"{message.from_user.username}, ввёл команду /start")
                await bot.send_message(message.from_user.id,
                                    f"Привет, @{message.from_user.username}\nЯ - бот для пополнения баланса.\nВаш счёт: {db.user_money(message.from_user.id)} руб. \nНажмите на кнопку, чтобы пополнить баланс",
                                    reply_markup=nav.topUpMenu)
            else:
                await bot.send_message(message.from_user.id,"Ты ЗАБЛОКИРОВАН!")
        else:
            if not db.check_ban_user(message.from_user.username):
                await bot.send_message(message.from_user.id,
                                   f"Привет, @{message.from_user.username}\nЯ - бот для пополнения баланса.\nВаш счёт: {db.user_money(message.from_user.id)} руб. \nНажмите на кнопку, чтобы пополнить баланс",
                                   reply_markup=nav.topUpMenu)
            else:
                await bot.send_message(message.from_user.id, "Ты ЗАБЛОКИРОВАН!")


    @dp.callback_query_handler(text="top_up")
    async def top_up(callback: types.CallbackQuery):
        await bot.delete_message(callback.from_user.id, callback.message.message_id)
        logger.debug(f"{message.from_user.username}, нажал кнопку ПОПОЛНИТЬ БАЛАНС")
        await bot.send_message(callback.from_user.id, "Введите сумму для пополнения!")
        await dialog.command.set()

        @dp.message_handler(state=dialog.command)
        async def bot_mess(message: types.Message, state: FSMContext):
            if message.chat.type == 'private':
                if message.text.upper() != 'ОТМЕНА':
                    if is_number(message.text):
                        message_money = int(message.text)
                        if message_money >= 10:
                            comment = str(message.from_user.id) + "_" + str(random.randint(1000, 9999))
                            bill = p2p.bill(amount=message_money, lifetime=5, comment=comment)

                            db.add_check(message.from_user.id, message_money, bill.bill_id)
                            logger.debug(f"{message.from_user.username}, ввёл сумму {message_money}")
                            await bot.send_message(message.from_user.id,
                                                   f'Вам нужно отправить {message_money} руб. на наш счёт QIWI\nСсылку:{bill.pay_url}\nУказанный комментарий к оплате: {comment}',
                                                   reply_markup=nav.buy_menu(url=bill.pay_url, bill=bill.bill_id))

                            await state.finish()
                        else:
                            logger.info(f"{message.from_user.username}, ввёл сумму {message.text} , меньше 10 руб.")
                            await bot.send_message(message.from_user.id,
                                                   "Минимальная сумма пополнения 10 руб. Чтобы прервать оплату напишите 'ОТМЕНА' ")
                    else:
                        logger.info(f"{message.from_user.username}, некорректно ввёл сумму {message.text}")
                        await bot.send_message(message.from_user.id,
                                               "Введите целое число. Чтобы прервать оплату напишите 'ОТМЕНА' ")
                else:
                    logger.info(f"{message.from_user.username}, ОТМЕНИЛ пополнение")
                    await bot.send_message(message.from_user.id, "Оплата ОТМЕНЕНА напишите '/start'")
                    await state.finish()

        @dp.callback_query_handler(text_contains="check_")
        async def check(callback: types.CallbackQuery):
            bill = str(callback.data)[6:]
            info = db.get_check(bill)
            if info != False:
                if str(p2p.check(bill_id=bill).status) == "PAID":
                    user_money = db.user_money(callback.from_user.id)
                    money = int(info[2])
                    db.set_money(callback.from_user.id, user_money + money)
                    db.delete_check(bill)
                    logger.debug(f"Пользователь {message.from_user.username} пополнил счёт на сумму{money}")
                    await bot.send_message(callback.from_user.id, "Вас счёт пополнен! Выполните команду /start.")
                else:
                    logger.info(f"Пользователь {message.from_user.username} не оплатил счёт")
                    await bot.send_message(callback.from_user.id, "Вы не оплатили счёт",
                                           reply_markup=nav.buy_menu(False, bill=bill))
            else:
                logger.info(f"Пользователь {message.from_user.username}, счёт не найден!")
                await bot.send_message(callback.from_user.id, "Счёт не найден")



def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(send_sticker_id, commands=['start'])
