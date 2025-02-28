from aiogram import Bot, Dispatcher, Router
from config.token import TOKEN
import sqlite3
from apscheduler.schedulers.asyncio import AsyncIOScheduler

con = sqlite3.connect("data/data.db")
cursor = con.cursor()

scheduler = AsyncIOScheduler(timezone='Europe/Moscow')

admin_id = [1375619533]

router = Router()
dp = Dispatcher()
dp.include_router(router)
bot = Bot(TOKEN)