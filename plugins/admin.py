import os
import json
import logging

logger = logging.getLogger(__name__)

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

# Baca konfigurasi dari config.json (relatif terhadap working directory)
with open("config.json", "r") as f:
    config = json.load(f)

OWNER_ID = config["owner_id"]
DATA_FILE = config.get("admin_file", "admin.json")  # fallback jika tidak ada

def save_admins(admins: set):
    """Simpan daftar admin ke file, tanpa menyertakan owner."""
    admins_to_save = admins - {OWNER_ID}
    with open(DATA_FILE, "w") as f:
        json.dump({"admins": list(admins_to_save)}, f, indent=2)

def load_admins():
    """Mengembalikan set ID admin (owner selalu otomatis masuk)."""
    if not os.path.exists(DATA_FILE):
        # Buat file baru dengan list kosong
        save_admins(set())
        return {OWNER_ID}

    try:
        with open(DATA_FILE, "r") as f:
            content = f.read().strip()
            if not content:
                # File kosong, tulis ulang
                save_admins(set())
                return {OWNER_ID}
            data = json.loads(content)
    except (json.JSONDecodeError, ValueError):
        # File rusak, backup dan reset
        backup_file = DATA_FILE + ".bak"
        if os.path.exists(backup_file):
            os.remove(backup_file)
        os.rename(DATA_FILE, backup_file)
        logger.warning(f"File {DATA_FILE} rusak, backup sebagai {backup_file}. Membuat baru.")
        save_admins(set())
        return {OWNER_ID}

    admins = set(data.get("admins", []))
    admins.add(OWNER_ID)   # owner selalu admin
    return admins

# Command: /addadmin <user_id>
async def add_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("⛔ Hanya pemilik bot yang bisa menambah admin.")
        return True

    if not context.args:
        await update.message.reply_text("ℹ️ Gunakan: /addadmin <user_id>")
        return True

    try:
        new_admin = int(context.args[0])
    except ValueError:
        await update.message.reply_text("❌ ID harus berupa angka.")
        return True

    admins = load_admins()
    if new_admin in admins:
        await update.message.reply_text("ℹ️ Pengguna tersebut sudah menjadi admin.")
        return True

    admins.add(new_admin)
    save_admins(admins)
    await update.message.reply_text(f"✅ User {new_admin} sekarang adalah admin.")
    return True

# Command: /removeadmin <user_id>
async def remove_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("⛔ Hanya pemilik bot yang bisa menghapus admin.")
        return True

    if not context.args:
        await update.message.reply_text("ℹ️ Gunakan: /removeadmin <user_id>")
        return True

    try:
        target = int(context.args[0])
    except ValueError:
        await update.message.reply_text("❌ ID harus berupa angka.")
        return True

    admins = load_admins()
    if target == OWNER_ID:
        await update.message.reply_text("❌ Pemilik bot tidak bisa dihapus.")
        return True
    if target not in admins:
        await update.message.reply_text("ℹ️ Pengguna tersebut bukan admin.")
        return True

    admins.remove(target)
    save_admins(admins)
    await update.message.reply_text(f"✅ User {target} telah dihapus dari admin.")
    return True

# Command: /listadmin
async def list_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    admins = load_admins()
    # Ambil username untuk tampilan lebih baik (tidak wajib)
    lines = []
    for uid in admins:
        try:
            user = await context.bot.get_chat(uid)
            name = user.first_name or user.username or str(uid)
        except:
            name = str(uid)
        lines.append(f"- {name} (`{uid}`)")
    text = "👑 <b>Daftar Admin</b>\n" + "\n".join(lines)
    await update.message.reply_text(text, parse_mode="HTML")
    return True

# Command: /owner
async def owner_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"🤖 Pemilik bot ini: `{OWNER_ID}`", parse_mode="MarkdownV2")
    return True

async def is_group_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Cek apakah pengirim adalah admin atau kreator di grup saat ini."""
    chat = update.effective_chat
    if chat.type == "private":
        await update.message.reply_text("ℹ️ Perintah ini hanya bisa digunakan di dalam grup.")
        return False
    user_id = update.effective_user.id
    try:
        member = await chat.get_member(user_id)
    except Exception:
        await update.message.reply_text("❌ Tidak dapat memverifikasi status.")
        return False
    if member.status in ["administrator", "creator"]:
        return True
    else:
        await update.message.reply_text("⛔ Anda bukan admin grup ini.")
        return False

def register(app):
    app.add_handler(CommandHandler("addadmin", add_admin))
    app.add_handler(CommandHandler("removeadmin", remove_admin))
    app.add_handler(CommandHandler("listadmin", list_admin))
    app.add_handler(CommandHandler("owner", owner_info))