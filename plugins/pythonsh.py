import json
import os
import subprocess
import sys
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

# Baca konfigurasi
with open("config.json", "r") as f:
    config = json.load(f)

OWNER_ID = config["owner_id"]
ADMIN_FILE = config.get("admin_file", "admin.json")


def is_bot_admin(user_id: int) -> bool:
    """Cek apakah user adalah superadmin (owner atau admin terdaftar)."""
    if user_id == OWNER_ID:
        return True
    if not os.path.exists(ADMIN_FILE):
        return False
    try:
        with open(ADMIN_FILE, "r") as f:
            data = json.load(f)
        return user_id in data.get("admins", [])
    except (json.JSONDecodeError, ValueError):
        return False


async def shell_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # Otorisasi
    if not is_bot_admin(user_id):
        await update.message.reply_text("⛔ Perintah ini hanya untuk superadmin bot.")
        return True

    if not context.args:
        await update.message.reply_text("ℹ️ Gunakan: /sh <perintah>\nContoh: /sh dir")
        return True

    command = " ".join(context.args)

    # Indikator mengetik
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

    output = ""
    try:
        if sys.platform == "win32":
            proc = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=10)
            output = proc.stdout or proc.stderr
        else:
            proc = subprocess.run(["sh", "-c", command], capture_output=True, text=True, timeout=10)
            output = proc.stdout + proc.stderr
    except subprocess.TimeoutExpired:
        output = "⏱️ Perintah melebihi batas waktu (10 detik)."
    except Exception as e:
        output = f"❌ Error: {type(e).__name__} - {e}"

    if not output.strip():
        output = "(tidak ada output)"
    if len(output) > 4000:
        output = output[:4000] + "\n\n... (dipotong)"

    # Kirim sebagai blok kode
    await update.message.reply_text(f"```\n{output}\n```", parse_mode="MarkdownV2")
    return True


def register(app):
    app.add_handler(CommandHandler("sh", shell_command))