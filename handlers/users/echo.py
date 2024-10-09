import aiohttp
import tempfile
from aiogram import types
from aiogram.types import InputFile
from loader import dp
from data.config import ADMINS

@dp.message_handler()
async def download_video_tiktok_ins_youtube(message: types.Message):
    # Yuklanayotganlik stikerini jo'natish
    url = "CAACAgEAAxkBAAIB_mUCIZT1b8f5gILnunw1CGjF9xQxAAKAAgACoWMZRKtYP6IFwk3cMAQ"
    downloading_message = await message.reply_sticker(url)
    text = message.text

    # Adminlarga xabarni forward qilish
    await message.forward(chat_id=ADMINS[0])

    try:
        # API'ga so'rov yuborish uchun URL va headerlar
        api_url = "https://auto-download-all-in-one.p.rapidapi.com/v1/social/autolink"
        payload = {"url": text}
        headers = {
            "content-type": "application/json",
            "X-RapidAPI-Key": "a89071279emsh52d6dfefe773534p1ef94ejsn4a8c42c2ddb2",
            "X-RapidAPI-Host": "auto-download-all-in-one.p.rapidapi.com"
        }

        # Asinxron API'ga POST so'rovi
        async with aiohttp.ClientSession() as session:
            async with session.post(api_url, json=payload, headers=headers) as response:
                response_json = await response.json()

        # API javobida media bor yoki yo'qligini tekshirish
        if response_json.get('medias'):
            medias = response_json['medias']
            media_type = response_json.get('type')

            # Agar Pinterest havolasi bo'lsa va ko'p rasm bo'lsa
            if media_type == 'multiple' and response_json['source'] == 'pinterest':
                await handle_single_pinterest_image(message, medias)

            # Boshqa manbalardan video yoki rasm yuklab olish
            else:
                media_url = medias[0]['url']  # Faqat birinchi media faylni olamiz
                media_format = medias[0].get('type')

                if media_format == 'image':
                    # Agar bu rasm bo'lsa, uni yuklab jo'natish
                    await download_and_send_image_async(media_url, message, caption="👉@fastyuklabot👈")

                elif media_format == 'video':
                    # Agar bu video bo'lsa, uni yuklab jo'natish
                    await download_and_send_video_async(media_url, message, caption="👉@fastyuklabot👈")

                else:
                    await message.answer("Qo'llab-quvvatlanmaydigan media turi.")
        else:
            await message.answer("Media topilmadi yoki URL noto'g'ri.")

    except Exception as e:
        # Xatolik yuz berganda foydalanuvchiga javob
        await message.answer(f"Xatolik yuz berdi: {str(e)}")

    # Yuklanayotgan stikerini o'chirish
    await downloading_message.delete()


async def handle_single_pinterest_image(message: types.Message, medias: list):
    """
    Pinterest havolalari uchun faqat bitta rasmni yuklab, jo'natish funksiyasi.
    """
    # Eng yuqori sifatli yoki birinchi rasmni tanlab olamiz
    first_image = medias[0]
    media_url = first_image['url']

    # Rasmni yuklab, foydalanuvchiga yuborish
    await download_and_send_image_async(media_url, message, caption="👉@fastyuklabot👈")


async def download_and_send_image_async(media_url: str, message: types.Message, caption: str):
    """
    Rasmni asinxron yuklab olish va foydalanuvchiga yuborish.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(media_url) as response:
            if response.status == 200:
                # Vaqtinchalik fayl yaratish
                with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp_file:
                    tmp_file.write(await response.read())  # Rasmni vaqtinchalik faylga yozish
                    tmp_file_path = tmp_file.name  # Fayl nomini olish

                # Rasmdan vaqtinchalik faylni yuklash
                await message.answer_photo(InputFile(tmp_file_path), caption=caption)
            else:
                await message.answer("Rasmni yuklab olishda xatolik yuz berdi.")


async def download_and_send_video_async(media_url: str, message: types.Message, caption: str):
    """
    Videoni asinxron yuklab olish va foydalanuvchiga yuborish.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(media_url) as response:
            if response.status == 200:
                # Vaqtinchalik fayl yaratish
                with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp_file:
                    tmp_file.write(await response.read())  # Videoni vaqtinchalik faylga yozish
                    tmp_file_path = tmp_file.name  # Fayl nomini olish

                # Videodan vaqtinchalik faylni yuklash
                await message.answer_video(InputFile(tmp_file_path), caption=caption)
            else:
                await message.answer("Videoni yuklab olishda xatolik yuz berdi.")
