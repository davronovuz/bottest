import requests
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import os
from dotenv import load_dotenv
from loader import dp,bot

# API orqali kontentni yuklab olish
def download_content_from_api(content_url):
    api_url = "https://auto-download-all-in-one.p.rapidapi.com/v1/social/autolink"
    payload = {"url": content_url}
    headers = {
        "x-rapidapi-key": "a89071279emsh52d6dfefe773534p1ef94ejsn4a8c42c2ddb2",
        "x-rapidapi-host": "auto-download-all-in-one.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    response = requests.post(api_url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()  # API'dan qaytgan javobni qaytaramiz
    else:
        return None


@dp.message_handler()
async def download_and_send_media(message: types.Message):
    content_url = message.text  # Foydalanuvchi yuborgan havola
    api_response = download_content_from_api(content_url)

    if api_response and not api_response.get("error"):
        # API javobidan birinchi media URL'ni olamiz (bu holda video bo'ladi)
        media_url = api_response['medias'][0]['url']
        media_type = api_response['medias'][0]['type']

        # Video yoki rasm yuborish
        if media_type == "video":
            await message.reply("Yuklanmoqda .....")
            await bot.send_video(message.chat.id, media=media_url)
        elif media_type == "image":
            await message.reply(" Yuklanmoqda .....")
            await bot.send_photo(message.chat.id, photo=media_url)
        else:
            await message.reply("Foydalanish mumkin bo'lgan media topilmadi.")
    else:
        await message.reply("Media yuklashda xatolik yuz berdi yoki noto'g'ri havola kiritildi.")


