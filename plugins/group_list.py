import json
import os
from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, filters, ContextTypes
from datetime import datetime

# Baca config untuk otorisasi
with open("config.json") as f:
    config = json.load(f)
OWNER_ID = config["owner_id"]
ADMIN_FILE = config.get("admin_file", "admin.json")

GROUPS_FILE = "groups.json"

# ========== FUNGSI BANTU (AMAN) ==========
def is_bot_admin(user_id: int) -> bool:
    if user_id == OWNER_ID:
        return True
    if not os.path.exists(ADMIN_FILE):
        return False
    try:
        with open(ADMIN_FILE) as f:
            data = json.load(f)
        return user_id in data.get("admins", [])
    except (json.JSONDecodeError, ValueError):
        return False

def load_groups():
    """Mengembalikan dict grup, tahan terhadap file kosong/rusak."""
    if not os.path.exists(GROUPS_FILE):
        return {}
    try:
        with open(GROUPS_FILE, "r") as f:
            content = f.read().strip()
            if not content:
                return {}
            return json.loads(content)
    except (json.JSONDecodeError, ValueError):
        # File rusak, backup dan reset
        backup = GROUPS_FILE + ".bak"
        if os.path.exists(backup):
            os.remove(backup)
        os.rename(GROUPS_FILE, backup)
        return {}

def save_groups(groups):
    with open(GROUPS_FILE, "w") as f:
        json.dump(groups, f, indent=2)

def update_group(chat_id, chat_title=None):
    groups = load_groups()
    chat_id = str(chat_id)
    if chat_id not in groups:
        groups[chat_id] = {
            "title": chat_title or "Unknown",
            "added": datetime.now().isoformat()
        }
    else:
        if chat_title:
            groups[chat_id]["title"] = chat_title
    save_groups(groups)

def remove_group(chat_id):
    groups = load_groups()
    if str(chat_id) in groups:
        del groups[str(chat_id)]
        save_groups(groups)

# ========== HANDLER ==========
async def track_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    if chat.type in ["group", "supergroup"]:
        update_group(chat.id, chat.title)
    return False   # jangan stop handler lain

async def bot_added(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    if chat.type in ["group", "supergroup"]:
        for member in update.message.new_chat_members:
            if member.id == context.bot.id:
                update_group(chat.id, chat.title)
                await update.message.reply_text("👋 Terima kasih telah mengundang saya! Gunakan /help untuk bantuan.")
                break
    return False

async def bot_removed(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.left_chat_member and update.message.left_chat_member.id == context.bot.id:
        remove_group(update.effective_chat.id)
    return False

async def list_groups(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_bot_admin(update.effective_user.id):
        await update.message.reply_text("⛔ Hanya superadmin yang bisa melihat daftar grup.")
        return True

    groups = load_groups()
    if not groups:
        await update.message.reply_text("📭 Bot belum berada di grup mana pun.")
        return True

    lines = [f"📋 <b>Daftar Grup ({len(groups)})</b>\n"]
    for chat_id, info in groups.items():
        title = info.get("title", "Tanpa Nama")
        lines.append(f"• <b>{title}</b> (<code>{chat_id}</code>)")

    text = "\n".join(lines)
    if len(text) > 4000:
        text = text[:4000] + "\n... (dipotong)"
    await update.message.reply_text(text, parse_mode="HTML")
    return True

# ========== REGISTER ==========
def register(app):
    app.add_handler(MessageHandler(filters.TEXT, track_group), group=2)
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, bot_added), group=2)
    app.add_handler(MessageHandler(filters.StatusUpdate.LEFT_CHAT_MEMBER, bot_removed), group=2)
    app.add_handler(CommandHandler("grouplist", list_groups))