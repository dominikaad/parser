from aiogram.types import Message
from loader import router, cursor, con, scheduler
from aiogram import F

@router.message(F.text == 'Просмотреть мои ссылки')
async def reg_start(message: Message):
    id_user = message.chat.id
    cursor.execute("SELECT url FROM users WHERE id = (?)", [id_user])
    a = cursor.fetchall()
    print(len(a))
    if not a:
        await message.answer(text='Вы ещё не добавляли ссылку')
        return
    #
    # for i in :
    #     await message.answer(text=f'Все ваши ссылки \n{i}.{a[i][0]}\n')