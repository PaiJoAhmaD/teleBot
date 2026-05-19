import json, os
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

with open("config.json") as f:
    config = json.load(f)
OWNER_ID = config["owner_id"]
ADMIN_FILE = config.get("admin_file", "admin.json")

def is_bot_admin(user_id):
    if user_id == OWNER_ID:
        return True
    if not os.path.exists(ADMIN_FILE):
        return False
    with open(ADMIN_FILE) as f:
        data = json.load(f)
    return user_id in data.get("admins", [])
    
def is_admin(user_id: int) -> bool:
    """Cek apakah user adalah admin atau owner bot."""
    if user_id == OWNER_ID:
        return True
    if not os.path.exists(ADMIN_FILE):
        return False
    with open(ADMIN_FILE, "r") as f:
        data = json.load(f)
    return user_id in data.get("admins", [])

# ================== HANDLER ==================
async def join_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Memberi tahu cara menambahkan bot ke grup lain."""
    bot_username = context.bot.username
    text = (
        "🤖 <b>Undang bot ke grup</b>\n\n"
        f"Klik tautan berikut:\n"
        f"https://t.me/{bot_username}?startgroup=true\n\n"
        "Atau:\n"
        f"1. Buka profil @{bot_username}\n"
        "2. Ketuk 'Tambahkan ke Grup'\n"
        "3. Pilih grup yang Anda kelola."
    )
    await update.message.reply_text(text, parse_mode="HTML")
    return True

async def leave_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Keluar dari grup saat ini (hanya admin bot)."""
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await update.message.reply_text("⛔ Perintah ini hanya untuk admin bot.")
        return True

    chat = update.effective_chat
    if chat.type == "private":
        await update.message.reply_text("ℹ️ Perintah ini hanya bisa digunakan di dalam grup.")
        return True

    try:
        await context.bot.leave_chat(chat.id)
        # Bot akan tetap mengirim pesan ini sebelum keluar
        await update.message.reply_text("👋 Bot telah meninggalkan grup.")
    except Exception as e:
        await update.message.reply_text(f"❌ Gagal keluar: {e}")

    return True

def register(app):
    app.add_handler(CommandHandler("join", join_info))
    app.add_handler(CommandHandler("leave", leave_group))