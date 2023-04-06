from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp, bot
from aiogram.dispatcher.filters import Text
from data_base import sqlite_db
from keyboards import admin_kb
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

ID = [513011135]


class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    discription = State()
    price = State()


# Получаем ID пользователя
# @dp.message_handler(commands=['moderator'], is_chat_admin=True)
async def make_changes_command(message: types.Message):
    global ID
    if message.from_user.id in ID:
        await bot.send_message(message.from_user.id, 'Что надо, хозяин?', reply_markup=admin_kb.button_case_admin)
    else:  # у тебя здесь нет власти
        await bot.send_sticker(message.chat.id,
                               'CAACAgIAAxkBAAIFtGLw6JmEUNd9nv4EpmLdfO2Sc13JAALrAAPww8AOBEFNY5iRmfUpBA')


# Начало диалога загрузки нового пункта меню
# @dp.message_handler(commands=['Download'], state=None)
async def cm_start(message: types.Message):
    if message.from_user.id in ID:
        await FSMAdmin.photo.set()
        await message.reply(f'Загрузи фото')


# Выход из состояния
# @dp.message_handler(state="*", commands='cancel')
# @dp.message_handler(Text(equals='отмена', ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    if message.from_user.id in ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply('OK')


# Ловим первый ответ и пишем в словарь
# @dp.message_handler(content_types=['photo'], state=FSMAdmin.photo)
async def laod_photo(message: types.Message, state: FSMContext):
    if message.from_user.id in ID:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await FSMAdmin.next()
        await message.reply('Теперь введи название')


# Ловим второй ответ
# @dp.message_handler(state=FSMAdmin.name)
async def load_name(message: types.Message, state: FSMContext):
    if message.from_user.id in ID:
        async with state.proxy() as data:
            data['name'] = message.text
        await FSMAdmin.next()
        await message.reply('Введи описание')


# Ловим третий ответ
# @dp.message_handler(state=FSMAdmin.discription)
async def load_discription(message: types.Message, state: FSMContext):
    if message.from_user.id in ID:
        async with state.proxy() as data:
            data['discription'] = message.text
        await FSMAdmin.next()
        await message.reply('Теперь укажи цену')


# Ловим последний ответ и используем полученные данные
# @dp.message_handler(state=FSMAdmin.price)
async def load_price(message: types.Message, state: FSMContext):
    if message.from_user.id in ID:
        async with state.proxy() as data:
            data['price'] = message.text
        await sqlite_db.sql_add_command(state)
        await state.finish()
        await message.reply('Отлично, сохранил!')


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('del '))
async def del_callback_run(callback_query: types.CallbackQuery):
    await sqlite_db.sql_delete_command(callback_query.data.replace('del ', ''))
    await callback_query.answer(text=f'{callback_query.data.replace("del ", "")} удалена', show_alert=True)


# @dp.message_handler(commands='Delete')
async def delete_item(message: types.Message):
    if message.from_user.id in ID:
        read = await sqlite_db.sql_read2()
        for ret in read:
            await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nОписание:\n{ret[2]}\nЦена:\n{ret[-1]}')
            await bot.send_message(message.from_user.id, text='👆', reply_markup=InlineKeyboardMarkup().\
                                   add(InlineKeyboardButton(f'Удалить {ret[1]}', callback_data=f'del {ret[1]}')))


async def command_look_uname(message: types.Message):
    if message.from_user.id in ID:
        await sqlite_db.look_username(message)


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(cm_start, commands=['Download'], state=None)
    dp.register_message_handler(cancel_handler, state="*", commands='cancel')
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(laod_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_discription, state=FSMAdmin.discription)
    dp.register_message_handler(load_price, state=FSMAdmin.price)
    dp.register_message_handler(make_changes_command, commands=['moderator'])  # , is_chat_admin=True)
    dp.register_message_handler(delete_item, commands=['Delete'])
    dp.register_message_handler(command_look_uname, commands=['users'])
