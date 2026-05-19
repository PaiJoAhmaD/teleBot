from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
import time
from datetime import timedelta

# asumsikan start_time diimpor dari bot.py
from bot import start_time  # atau simpan di tempat lain

async def uptime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    delta = timedelta(seconds=int(time.time() - start_time))
    await update.message.reply_text(f"⏱ Bot sudah berjalan selama: {delta}")
    return True

def register(app):
    app.add_handler(CommandHandler("uptime", uptime))