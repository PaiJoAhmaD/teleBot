from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

DAFTAR_PERINTAH = """
📜 <b>Daftar Perintah Bot</b>

<b>Umum:</b>
/start – Memulai bot
/help – Bantuan singkat
/perintah – Lihat daftar ini
/id – Cek ID pengguna & chat
/ping – Cek status bot
/uptime – Lama bot berjalan

<b>Fitur:</b>
/cuaca [kota] – Info cuaca
/hitung [ekspresi] – Kalkulator (via mention: @bot hitung 5+3)

<b>Admin Grup:</b>
/cekbot – Cek izin bot di grup
/cekuser [@user/ID] – Cek status user

<b>Admin Bot (khusus admin):</b>
/sh [perintah] – Jalankan shell (hanya admin bot)
/addadmin [ID] – Tambah admin bot (owner only)
/removeadmin [ID] – Hapus admin bot (owner only)
/listadmin – Daftar admin bot
/owner – Info pemilik bot
"""

async def perintah(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(DAFTAR_PERINTAH, parse_mode="HTML")
    return True

def register(app):
    app.add_handler(CommandHandler("perintah", perintah))