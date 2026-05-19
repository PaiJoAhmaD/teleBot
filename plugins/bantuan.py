from telegram import Update
from telegram.ext import MessageHandler, filters, ContextTypes

async def bantuan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📖 Fitur:\n"
        "- halo / hai\n"
        "- bantuan\n"
        "- pesan [produk]\n"
        "- alamat\n"
        "- hitung [ekspresi] (contoh: hitung 9-8)\n"
        "- /cuaca [kota]"
    )

def register(app):
    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND & filters.Regex(r'\b(bantuan|help|fitur|perintah)\b'),
        bantuan,
    ))