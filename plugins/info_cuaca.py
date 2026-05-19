# plugins/info_cuaca.py
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

async def cuaca(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kota = " ".join(context.args) if context.args else "Jakarta"
    # Simulasi data cuaca (bisa diganti dengan API sungguhan)
    await update.message.reply_text(f"🌤️ Cuaca di {kota}: Cerah, 28°C")

def register(app):
    """Fungsi ini dipanggil oleh bot utama untuk mendaftarkan handler."""
    app.add_handler(CommandHandler("cuaca", cuaca))