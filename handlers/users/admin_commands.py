from loader import dp,db,bot
from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from states.admin_state import ReklamaState,AddChannelState,DeleteChannelState
from data.config import ADMINS

from keyboards.default.reply_keyboards import admin_btn, channels_btn,exit_btn


@dp.message_handler(commands="admin")
async def admin_handler(msg: types.Message):
    if str(msg.from_user.id) not in ADMINS:
        await msg.answer("Siz admin emassiz ❌", reply_markup=types.ReplyKeyboardRemove())
        return  # Admin bo'lmagan foydalanuvchini qaytarish

    await msg.answer(f"Assalomu alaykum {msg.from_user.first_name} 🤖\nAdmin sahifaga xush kelibsiz ⚙️",
                     reply_markup=admin_btn())


@dp.message_handler(Text("Statistika 📊"))
async def user_statistika_handler(msg: types.Message):
    if str(msg.from_user.id) in ADMINS:
        await msg.answer(text= f"Bazada {db.count_users()} ta foydalanuvchi bor", reply_markup=admin_btn())
    else:
        await msg.answer("Siz admin emassiz ❌", reply_markup=types.ReplyKeyboardRemove())




@dp.message_handler(Text("Reklama 🎁"))
async def reklama_handler(msg: types.Message):
    if str(msg.from_user.id) in ADMINS:
        await ReklamaState.rek.set()
        await bot.send_message(chat_id=msg.chat.id, text="Reklama tarqatish bo'limi 🤖", reply_markup=exit_btn())
    else:
        await bot.send_message(chat_id=msg.chat.id, text="Siz admin emassiz ❌",
                               reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler(state=ReklamaState.rek, content_types=types.ContentType.ANY)
async def rek_state(msg: types.Message, state: FSMContext):
    if msg.text == "❌":
        await bot.send_message(chat_id=msg.chat.id, text="Reklama yuborish bekor qilindi 🤖❌", reply_markup=admin_btn())
        await state.finish()
    else:
        await bot.send_message(chat_id=msg.chat.id, text="Reklama yuborish boshlandi 🤖✅", reply_markup=admin_btn())
        await state.finish()
        try:
            summa = 0
            for user in db.select_all_users():
                user_id = int(user[1])
                if user_id not in [int(admin) for admin in ADMINS]:
                    try:
                        await msg.copy_to(user_id, caption=msg.caption,
                                          caption_entities=msg.caption_entities, reply_markup=msg.reply_markup)
                    except Exception as e:
                        print(f"Send Error: {e}")
                        summa += 1

            for admin in ADMINS:
                await bot.send_message(int(admin), text=f"Botni bloklagan Userlar soni: {summa}")
        except Exception as e:
            print(f"Error: {e}")




@dp.message_handler(Text("❌"))
async def exit_handler(msg: types.Message):
    for admin in ADMINS:
        if msg.from_user.id == int(admin):
            await msg.answer("Bosh menyu 🔮", reply_markup=admin_btn())
