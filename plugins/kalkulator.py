# plugins/kalkulator.py

import re
from telegram import Update
from telegram.constants import ChatAction      # ✅ impor dari constants
from telegram.ext import MessageHandler, filters, ContextTypes
import asyncio

async def hitung(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Indikator mengetik
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    await asyncio.sleep(0.5)  # opsional, biar terlihat memproses

    teks = update.message.text
    teks_bersih = re.sub(r'@\w+', '', teks).strip()
    match = re.search(r'(?:hitung|kalkulator)\s+(.+)', teks_bersih, re.IGNORECASE)
    if match:
        ekspresi = match.group(1)
        try:
            if re.match(r'^[\d\s+\-*/().]+$', ekspresi):
                hasil = eval(ekspresi)
                await update.message.reply_text(f"🧮 Hasil: {hasil}")
                return True
        except:
            await update.message.reply_text("⚠️ Ekspresi tidak valid.")
            return True
    else:
        await update.message.reply_text("Gunakan format: hitung <ekspresi>")
        return True

def register(app):
    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND & filters.Regex(r'\b(hitung|kalkulator)\b'),
        hitung,
    ))