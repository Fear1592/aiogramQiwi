from aiogram import executor
from create_bot import dp

from handlers import client, admin


client.register_handlers_client(dp)
admin.register_message_handlers_admin(dp)

# @dp.message_handler()
# async def new_money(message: types.Message):
#     if message.chat.type == 'private':
#         await bot.send_message(message.from_user.id, "Сумма введена")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, )
