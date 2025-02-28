from aiogram.types import Message
from loader import router, cursor, con, scheduler
from aiogram import F

@router.message(F.text == 'Удалить ссылку')
async def reg_start(message: Message):
    id_user = message.chat.id
    cursor.execute("SELECT id FROM users WHERE id = (?)", [id_user])
    a = cursor.fetchall()
    if not a:
        await message.answer(text='Вы ещё не добавляли ссылку')
        return
    cursor.execute("SELECT id_task FROM users WHERE id = (?)", [id_user])
    b = cursor.fetchall()
    scheduler.remove_job(b[0])
    cursor.execute(
        "DELETE * FROM users WHERE id = (?) ", [id_user])
    con.commit()