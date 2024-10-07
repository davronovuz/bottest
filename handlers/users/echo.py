from aiogram import types
from  loader import dp,bot
from data.config import ADMINS


@dp.message_handler()
async def bot_echo(message: types.Message):
    user_text = message.text
    user_username=message.from_user.username
    user_fullname=message.from_user.full_name
    user_id=message.from_user.id

    msg=f"Qadrli Admin foydalanuvchi  {message.from_user.full_name} botga xabar yubordi\n"
    msg+=f"foydalanuvchi haqida malumot:\n"
    msg+=f"Username: @{user_username}\n"
    msg+=f"Fullname: {user_fullname}\n"
    msg+=f"ID: {user_id}\n"
    msg+=f"Xabar: {user_text}"
    for admin in ADMINS:
        await bot.send_message(chat_id=admin,text=msg)