from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import dp, bot, db, cfg, logger
import keyboards.admin_kb as nav


class admin_command(StatesGroup):
    add_user = State()
    new_user_money = State()
    ban_user = State()


def is_number(_str):
    try:
        int(_str)
        return True
    except ValueError:
        return False


@logger.catch
async def admin_panel(message: types.Message):
    if message.chat.type == 'private':
        user_admin = str(message.from_user.username) + str(message.from_user.id)
        if user_admin == cfg.ADMIN:
            logger.info(f"Администратор {message.from_user.username}, зашёл в админу")
            await bot.send_message(chat_id=message.from_user.id,
                                   text=f"Привет {message.from_user.username}. Ваш ID: {message.from_user.id}, ты админ!",
                                   reply_markup=nav.get_keyboard())
        else:
            logger.info(f"Пользователь попытался зайти в админку {message.from_user.username}")
            await bot.send_message(chat_id=message.from_user.id,
                                   text=f"Ваш ID: {message.from_user.username}{message.from_user.id}")


@dp.callback_query_handler(text="all_balance")
async def all_balance(callback: types.CallbackQuery):
    await bot.delete_message(callback.from_user.id, callback.message.message_id)
    all = db.show_all()
    list_money = ""
    for i, j in all:
        list_money += f"Пользователь: {i},  Баланс составляет: {j} руб.\n"
    logger.info(f"Администратор {callback.from_user.username} Нажал кнопку ПРОВЕРИТЬ БАЛАНС ПОЛЬЗОВАТЕЛЕЙ")
    await bot.send_message(callback.from_user.id, list_money)


@dp.callback_query_handler(text="update_balance", )
async def update_balance(callback: types.CallbackQuery):
    logger.info(f"Администратор {callback.from_user.username}, нажал кнопку для изминения баланса")
    await bot.send_message(callback.from_user.id, "Введите ник пользователя")
    await admin_command.add_user.set()

    @dp.message_handler(state=admin_command.add_user)
    async def check_user_name(message: types.Message, state: FSMContext):
        if message.chat.type == 'private':
            if message.text.upper() != 'ОТМЕНА':
                if db.admin_check(message.text):
                    async with state.proxy() as data:
                        data['user_name'] = message.text
                        logger.info(
                            f"Администратор {callback.from_user.username}, ввёл ник пользователя {message.text} ")
                        await bot.send_message(message.from_user.id,
                                               "Пользователь найден введите сумму для изминение, или напиши ОТМЕНА")
                        await admin_command.next()
                else:
                    logger.info(
                        f"Администратор {callback.from_user.username}, ввёл ник пользователя {message.text} ПОЛЬЗОВАТЕЛЬ НЕ НАЙДЕН!! ")
                    await bot.send_message(message.from_user.id,
                                           "Пользователь не найден! Попробуй ещё раз или напиши 'ОТМЕНА'")
            else:
                logger.info(
                    f"Администратор {callback.from_user.username}, ОТМЕНИЛ изминения баланса пользователя ")
                await bot.send_message(message.from_user.id, "Операция ОТМЕНЕНА!")
                await state.finish()

    @dp.message_handler(state=admin_command.new_user_money)
    async def new_balance_user(message: types.Message, state: FSMContext):
        if message.chat.type == 'private':
            if message.text.upper() != 'ОТМЕНА':
                if is_number(message.text):
                    async with state.proxy() as data:
                        user_name = data['user_name']
                        money_new = int(message.text)
                        logger.info(
                            f"Администратор {callback.from_user.username}, изменил у пользователя {user_name}\nСумма: {money_new} руб. ")
                        await bot.send_message(message.from_user.id,
                                               f"Сумма успешно изменина!\nПользователь: {user_name}\nСумма: {money_new} руб.")
                        await state.finish()
                        db.admin_set_money(user_name=user_name, money=money_new)

                else:
                    logger.info(
                        f"Администратор {callback.from_user.username}, неккоректно ввёл сумму {message.text} ")
                    await bot.send_message(message.from_user.id,
                                           "Введите целое число. Чтобы прервать процесс напишите 'ОТМЕНА' ")
            else:
                await bot.send_message(message.from_user.id, "Вы ОТМЕНИЛИ напишите '/start'")
                await state.finish()


@dp.callback_query_handler(text="block_user", )
async def update_balance(callback: types.CallbackQuery):
    logger.info(
        f"Администратор {callback.from_user.username}, нажал кнопку ЗАБЛОКИРОВАТЬ ИЛИ РАЗБЛОКИРОВАТЬ пользователя")
    await bot.send_message(callback.from_user.id, "Введите ник пользователя, для БЛОКИРОВКИ или РАЗБЛОКИРОВКИ")
    await admin_command.ban_user.set()

    @dp.message_handler(state=admin_command.ban_user)
    async def check_user_name(message: types.Message, state: FSMContext):
        if message.text.upper() != 'ОТМЕНА':
            if db.admin_check(message.text):
                db.check_ban_user(user_name=message.text)
                await bot.send_message(message.from_user.id, f"Пользователь найден! {message.text}")
                if db.check_ban_user(message.text) == True:
                    logger.info(
                        f"Администратор {callback.from_user.username}, ЗАБЛОКИРОВАННЫЙ {message.text} НАЙДЕН")
                    await bot.send_message(message.from_user.id,
                                           f"Пользователь {message.text} уже ЗАБЛОКИРОВАН хотите РАЗБЛОКИРОВАТЬ?",
                                           reply_markup=nav.topUnBanned)
                    await state.finish()
                else:
                    logger.info(
                        f"Администратор {callback.from_user.username}, ПОЛЬЗОВАТЕЛЬ НАЙДЕН{message.text} НАЙДЕН")
                    await bot.send_message(message.from_user.id,
                                           f"ЗАБЛОКИРОВАТЬ ПОЛЬЗОВАТЕЛЯ {message.text}?",
                                           reply_markup=nav.topBanned)
                    await state.finish()
            else:
                logger.info(
                    f"Администратор {callback.from_user.username}, пользователь не найдён!")
                await bot.send_message(message.from_user.id, f"Пользователь не найден")
        else:
            logger.info(
                f"Администратор {callback.from_user.username}, вышел из меню блокировки")
            await bot.send_message(message.from_user.id, f"Блокировка отменена")
            await state.finish()

        @dp.callback_query_handler(text="banned")
        async def ban_user(callback: types.CallbackQuery):
            user_name = message.text
            db.ban_set_user(user_name=user_name, is_banned=True)
            logger.info(
                f"Администратор {callback.from_user.username}, ЗАБЛОКИРОВАЛ пользователя {user_name}")
            await bot.send_message(callback.from_user.id,
                                   f"Пользователь {user_name} ЗАБЛОКИРОВАН!")

        @dp.callback_query_handler(text="unbanned")
        async def unban_user(callback: types.CallbackQuery):
            user_name = message.text
            db.ban_set_user(user_name=user_name, is_banned=False)
            logger.info(
                f"Администратор {callback.from_user.username}, РАЗБЛОКИРОВАЛ пользователя {user_name}")
            await bot.send_message(callback.from_user.id,
                                   f"Пользователь {user_name} РАЗБЛОКИРОВАН")


@dp.callback_query_handler(text="show_logs")
async def update_balance(callback: types.CallbackQuery):
    logger.info(
        f"Администратор {callback.from_user.username}, зашёл в выгрузку логов")
    await bot.send_message(callback.from_user.id, "ВЫБЕРИ ФАЙЛ ДЛЯ ВЫГРУЗКИ", reply_markup=nav.get_keyboard_logs())


    @dp.callback_query_handler(text="debug_logs")
    async def logs_debug(callback: types.CallbackQuery):
        logger.info(
            f"Администратор {callback.from_user.username}, выгрузил файл DEBUG логов")
        await bot.send_document(callback.from_user.id, open('debug.json', 'rb'))

    @dp.callback_query_handler(text="warning_logs")
    async def logs_warning(callback: types.CallbackQuery):
        logger.info(
            f"Администратор {callback.from_user.username}, выгрузил файл WARNING логов")
        await bot.send_document(callback.from_user.id, open('warning.json', 'rb'))





def register_message_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(admin_panel, commands=['admin']),
