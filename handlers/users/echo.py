import io
from aiogram import types
from loader import dp
import requests
from data.config import ADMINS

@dp.message_handler()
async def download_video_tiktok_ins_youtube(message: types.Message):
    url="CAACAgEAAxkBAAIB_mUCIZT1b8f5gILnunw1CGjF9xQxAAKAAgACoWMZRKtYP6IFwk3cMAQ"
    downloading_message = await message.reply_sticker(url)
    text = message.text
    await message.forward(chat_id=ADMINS[0])

    try:
        url = "https://auto-download-all-in-one.p.rapidapi.com/v1/social/autolink"

        payload = {
            "url": text
        }
        headers = {
            "content-type": "application/json",
            "X-RapidAPI-Key": "a89071279emsh52d6dfefe773534p1ef94ejsn4a8c42c2ddb2",
            "X-RapidAPI-Host": "auto-download-all-in-one.p.rapidapi.com"
        }

        response = requests.post(url, json=payload, headers=headers)
        response = response.json()
        video = response['medias'][0]['url']
        title = response['title']
        title+=f"\n\n 👉@fastyuklabot👈"

        if video:
            video_response = requests.get(video)
            if video_response.status_code == 200:
                video_file = io.BytesIO(video_response.content)
                # Yuklab olingan video bilan chiroyli xabarini yuborish
                await message.answer_video(video_file, caption=title)
            else:
                await message.answer("Videoni yuklab olishda xatolik yuz berdi. Qayta harakat qiling.")
        else:
            await message.answer("Video manzilida xatolik bor.")

    except:
            await message.answer("Iltimos, botga  faqat video url yuboring")


    await downloading_message.delete()


