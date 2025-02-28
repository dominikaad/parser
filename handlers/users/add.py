from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from keys.key import kb_start
from loader import router, cursor, con, scheduler, bot
from aiogram import F
from script.parser import parser_update, parse_website
import json

class FormUrl(StatesGroup):
    url = State()

@router.message(F.text == 'Добавить ссылку')
async def reg_start(message: Message, state: FSMContext):
    id_user = message.chat.id
    cursor.execute("SELECT id FROM users WHERE id = (?)", [id_user])
    a = cursor.fetchall()
    if a:
        await message.answer(text='Вы уже добавляли ссылку')
        return
    await state.set_state(FormUrl.url)
    await message.answer('Введите ссылку', reply_markup=types.ReplyKeyboardRemove())

@router.message(FormUrl.url)
async def reg_start(message: Message, state: FSMContext):
    await state.update_data(url=message.text)
    data = await state.get_data()
    url = data['url']
    id_user = message.chat.id
    await state.clear()
    task = scheduler.add_job(parser_update,
                             trigger='interval',
                             seconds=60,
                             kwargs={'user_id': id_user, 'bot': bot})
    id_task = task.id
    cursor.execute(
        "INSERT INTO users (id, url, id_task) VALUES (?, ?, ?)",
        [id_user, url, id_task])
    con.commit()
    await message.answer('Ваша ссылка принята')

