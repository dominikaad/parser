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
    desc = State()

@router.message(F.text == 'Добавить ссылку')
async def reg_start(message: Message, state: FSMContext):
    id_user = message.chat.id
    cursor.execute("SELECT id FROM users WHERE id = (?)", [id_user])
    a = cursor.fetchall()
    await state.set_state(FormUrl.desc)
    await message.answer('Введите описание ссылки (одно английское слово, описсывающее продук)', reply_markup=types.ReplyKeyboardRemove())

@router.message(FormUrl.desc)
async def get_desc(message: Message, state: FSMContext):
    await state.update_data(desc=message.text)
    await state.set_state(FormUrl.url)
    await message.answer('Введите вашу ссылку')


@router.message(FormUrl.url)
async def reg_start(message: Message, state: FSMContext):
    await state.update_data(url=message.text)
    data = await state.get_data()
    url = data['url']
    desc = data['desc']
    id_user = message.chat.id
    await state.clear()
    task = scheduler.add_job(parser_update,
                             trigger='interval',
                             seconds=60,
                             kwargs={'user_id': id_user, 'desc': desc, 'bot': bot})
    id_task = task.id
    cursor.execute(
        "INSERT INTO users (id, url, id_task, description) VALUES (?, ?, ?, ?)",
        [id_user, url, id_task, desc])
    con.commit()
    await message.answer('Ваша ссылка принята')
    class_names = 'styles_wrapper__5FoK7'
    inner_class_name = "styles_secondary__MzdEb"
    result = parse_website(data['url'], class_names, inner_class_name)[:5]
    with open(f'data/{id_user}_{desc}.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(result))
