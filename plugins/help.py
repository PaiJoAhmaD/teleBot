from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, filters, ContextTypes

BANTUAN_LENGKAP = """
📖 <b>Bantuan Bot</b>

Ketik /perintah untuk daftar semua perintah.
Atau sebut saya dengan kata kunci:
• halo / hai → sapaan
• bantuan → lihat ini
• pesan [produk] → info pemesanan
• alamat → lokasi
• hitung [ekspresi] → kalkulator (contoh: hitung 5+3)
"""

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(BANTUAN_LENGKAP, parse_mode="HTML")
    return True

async def help_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await help_command(update, context)
    return True

def register(app):
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND & filters.Regex(r'\b(help|bantuan)\b'),
        help_message
    ))