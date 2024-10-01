from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
import logging

from data.config import ADMINS
from loader import dp, db


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    try:
        telegram_id = message.from_user.id
        username = message.from_user.username

        # Foydalanuvchi allaqachon mavjudligini tekshirish
        if not db.select_user(telegram_id=telegram_id):
            db.add_user(telegram_id, username)
            logging.info(f"Foydalanuvchi qo'shildi: {telegram_id=} {username=}")

        count = db.count_users()
        for admin in ADMINS:
            await dp.bot.send_message(
                admin,
                f"Telegram ID: {telegram_id}\n"
                f"Username: @{username}\n"
                f"To'liq ismi: {message.from_user.full_name}\n"
                f"Foydalanuvchi bazaga qo'shildi.\n\n"
                f"Bazada <b>{count[0]}</b> ta foydalanuvchi bor."
            )

        # Foydalanuvchiga xush kelibsiz matni yuborish
        text = (
            "Assalomu alaykum, xush kelibsiz! 👋\n\n"
            "Ushbu bot yordamida siz Instagram, TikTok, Pinterest, Facebook, va Snapchat platformalaridan "
            "video va rasm yuklab olishingiz mumkin.\n\n"
            "Iltimos, kerakli platformadan havolani botga yuboring."
        )
        await message.answer(text)

    except Exception as err:
        logging.exception(err)
