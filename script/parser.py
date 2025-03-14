import requests
from aiogram.types import WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bs4 import BeautifulSoup
from loader import cursor, Bot
import json
from aiogram import types


def parse_website(url, class_names, inner_class_name):
    response = requests.get(url)
    if response.status_code != 200:
        print(f'Ошибка запроса: {response.status_code}')
        return None
    soup = BeautifulSoup(response.text, 'html.parser')
    parser_data = []
    elements = soup.find_all(class_=class_names)
    for element in elements:
        text = element.get_text(strip=True)

        img_tag = element.find('img')
        img_url = img_tag['src'] if img_tag and 'src' in img_tag.attrs else None

        inner_element = element.find(class_=inner_class_name)
        inner_text = inner_element.get_text(strip=True) if inner_element else None

        link_url = element.get('href') if element.has_attr('href') else None
        link_url = link_url.split('?')[0]

        parser_data.append([text, img_url, inner_text, link_url])
        return parser_data


async def parser_update(user_id, desc, bot: Bot):
    cursor.execute("SELECT * FROM users WHERE id = (?) AND description = (?)", [user_id, desc])
    a = cursor.fetchall()
    class_names = 'styles_wrapper__5FoK7'
    inner_class_name = "styles_secondary__MzdEb"
    url = a[0][1]
    result = parse_website(url, class_names, inner_class_name)[:5]
    with open(f'data/{user_id}_{desc}.json', 'r', encoding='utf-8') as file:
        old_result = json.loads(file.read())

    new_hran = []
    for item in result:
        if item not in old_result:
            new_hran.append(item)
    print(new_hran)
    if new_hran:
        with open(f'data/{user_id}_{desc}.json', 'w', encoding='utf-8') as file:
            file.write(json.dumps(result))
        for mess in new_hran:
            builder = InlineKeyboardBuilder()
            builder.add(types.InlineKeyboardButton(text='открыть обьявления',
                                                   web_app=WebAppInfo(url=mess[3])))
            await bot.send_photo(caption=f'{mess[0]}\n{mess[2]}',
                                 chat_id=user_id, photo=mess[1],
                                 reply_markup=builder.as_markup(resize_keyboard=True))
