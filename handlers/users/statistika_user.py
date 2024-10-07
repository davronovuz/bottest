from aiogram import types
from datetime import datetime, timedelta
from loader import dp,db

# Statistika handler
@dp.message_handler(commands="Statistika 📊")
async def send_statistics(message: types.Message):
    today = datetime.now()
    daily_date = today - timedelta(days=1)   # So'nggi 1 kun
    weekly_date = today - timedelta(weeks=1)  # So'nggi 1 hafta
    monthly_date = today - timedelta(days=30)  # So'nggi 1 oy

    # Kundalik foydalanuvchilar soni
    daily_users = db.execute(
        "SELECT COUNT(*) FROM Users WHERE created_at >= ?",
        parameters=(daily_date,), fetchone=True
    )[0]

    # Haftalik foydalanuvchilar soni
    weekly_users = db.execute(
        "SELECT COUNT(*) FROM Users WHERE created_at >= ?",
        parameters=(weekly_date,), fetchone=True
    )[0]

    # Oylik foydalanuvchilar soni
    monthly_users = db.execute(
        "SELECT COUNT(*) FROM Users WHERE created_at >= ?",
        parameters=(monthly_date,), fetchone=True
    )[0]

    total_users = db.count_users()[0]  # Umumiy foydalanuvchilar soni

    # Javob
    stats_message = (
        f"📊 Statistika:\n\n"
        f"🟢 Kunlik foydalanuvchilar: {daily_users}\n"
        f"🔵 Haftalik foydalanuvchilar: {weekly_users}\n"
        f"🟣 Oylik foydalanuvchilar: {monthly_users}\n"
        f"⚫️ Umumiy foydalanuvchilar: {total_users}"
    )

    await message.answer(stats_message)