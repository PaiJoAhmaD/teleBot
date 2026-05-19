from telegram import Update
from telegram.ext import MessageHandler, filters, ContextTypes

async def sapaan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Halo {update.effective_user.first_name}!")

def register(app):
    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND & filters.Regex(r'\b(halo|hai|pagi|siang|malam|assalamualaikum)\b'),
        sapaan,
    ))