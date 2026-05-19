from telegram import Update
from telegram.ext import MessageHandler, filters, ContextTypes

async def pemesanan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Untuk memesan, ketik 'pesan [nama produk]'. Contoh: pesan kopi susu")

def register(app):
    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND & filters.Regex(r'\b(harga|beli|pesan|order)\b'),
        pemesanan,
    ))