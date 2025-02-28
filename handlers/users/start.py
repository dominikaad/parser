from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from keys.key import kb_start
from loader import router, cursor, con


@router.message(Command('start'))
async def fun_start (message: Message):
    builder = ReplyKeyboardBuilder()
    for button in kb_start:
        builder.add(button)
    builder.adjust(1)
    await message.answer(text='Йоу бро',
                         reply_markup=builder.as_markup(resize_keyboard=True))

