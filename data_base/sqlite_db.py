import sqlite3 as sq
from create_bot import bot


def sql_start():
    global base, cur
    base = sq.connect('orders.db')
    cur = base.cursor()
    if base:
        print('DB connected OK!')
    base.execute('CREATE TABLE IF NOT EXISTS menu(img TEXT, name TEXT PRIMARY KEY, description TEXT, price TEXT)')
    base.execute('CREATE TABLE IF NOT EXISTS users_id(id INTEGER PRIMARY KEY, date TEXT, uid INTEGER)')
    base.execute('CREATE TABLE IF NOT EXISTS username(id INTEGER PRIMARY KEY, date TEXT, uname TEXT)')
    base.commit()


async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO menu VALUES (?, ?, ? , ?)', tuple(data.values()))
        base.commit()


async def sql_add_user_id(date, message):
    cur.execute('INSERT INTO users_id (date, uid) VALUES (?, ?)', (date, message))
    base.commit()


async def sql_add_user_name(date, message):
    cur.execute('INSERT INTO username (date, uname) VALUES (?, ?)', (date, message))
    base.commit()


async def sql_read(message):
    for ret in cur.execute('SELECT * FROM menu').fetchall():
        await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\n\nОписание:\n{ret[2]}\n\nЦена:\n{ret[-1]}')


async def sql_read2():
    return cur.execute('SELECT * FROM menu').fetchall()


async def look_id(message):
    answer = cur.execute('SELECT uid FROM users_id').fetchall()
    s = set()
    for i in answer:
        s.add(i)
    await bot.send_message(message.from_user.id, f'Количество подписчиков: {len(s)}')


async def look_username(message):
    answer = cur.execute('SELECT uname FROM username').fetchall()
    s = set()
    for i in answer:
        s.add(i[0])
    for j in s:
        await bot.send_message(message.from_user.id, f'Подписчик: @{j}')


async def sql_delete_command(data):
    cur.execute('DELETE FROM menu WHERE name == ?', (data,))
    base.commit()
