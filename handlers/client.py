from aiogram import types, Dispatcher
from create_bot import bot
from keyboards import kb_client
from data_base import sqlite_db
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime


# @dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
    await bot.send_message(message.from_user.id, f'Удачной сделки!')  # , reply_markup=kb_client)
    date = datetime.now().strftime("%d-%m-%Y %H:%M")
    await sqlite_db.sql_add_user_id(date, message.from_user.id)
    await sqlite_db.sql_add_user_name(date, message.from_user.username)


async def command_work_mode(message: types.Message):
    await bot.send_message(message.from_user.id, f'Режим работы магазина:\n'
                                                 f'Пн-Пт с 9:00 до 18:00;\n'
                                                 f'Сб-Вс с 12:00 до 16:00.')


async def command_location(message: types.Message):
    await bot.send_message(message.from_user.id, f'Ставропольский край, город Невинномысск')


async def command_menu(message: types.Message):
    await sqlite_db.sql_read(message)


async def command_look_id(message: types.Message):
    await sqlite_db.look_id(message)


# кнопка ссылка
urlkb = InlineKeyboardMarkup(row_width=1)
url_button_0 = InlineKeyboardButton(text='Разработчик ботов', url='https://t.me/Setochkin')
url_button_1 = InlineKeyboardButton(text='БОТ тренажер памяти', url='https://t.me/memoryxxxbot')
url_button_2 = InlineKeyboardButton(text='Каталог Telegram-каналов и чатов', url='https://tgstat.ru/')
url_button_3 = InlineKeyboardButton(text='Телеграм Роботы', url='https://tgram.ru/bots')
url_button_4 = InlineKeyboardButton(text='Биржа Telegram-ботов', url='https://botstat.io')
urlkb.add(url_button_0, url_button_1, url_button_2, url_button_3, url_button_4)


# @dp.message_handler(commands='links')
async def url_command(message: types.Message):
    await message.answer('Полезные ссылки: ', reply_markup=urlkb)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(command_work_mode, commands=['РЕЖИМ_РАБОТЫ'])
    dp.register_message_handler(command_location, commands=['МЕСТО_НАХОЖДЕНИЯ'])
    dp.register_message_handler(command_menu, commands=['menu'])
    dp.register_message_handler(url_command, commands=['links'])
    dp.register_message_handler(command_look_id, commands=['id'])
