from telegram import Update
from telegram.ext import MessageHandler, filters, ContextTypes

async def alamat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📍 Kantor kami di Jl. Merdeka No.123")

def register(app):
    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND & filters.Regex(r'\b(alamat|maps|lokasi|kantor)\b'),
        alamat,
    ))