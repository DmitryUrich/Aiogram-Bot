from aiogram import types, Dispatcher
from create_bot import dp, bot


# @dp.message_handler()
async def echo(message: types.Message):
    await bot.send_message(message.from_user.id, message.text)


def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(echo)
