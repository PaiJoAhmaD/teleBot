from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    text = f"🆔 User ID: `{user_id}`\n💬 Chat ID: `{chat_id}`"
    await update.message.reply_text(text, parse_mode="MarkdownV2")
    return True

def register(app):
    app.add_handler(CommandHandler("id", get_id))