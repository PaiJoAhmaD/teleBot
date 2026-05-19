from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot siap! Ketik /ping untuk cek status.")
    return True

def register(app):
    app.add_handler(CommandHandler("start", start))