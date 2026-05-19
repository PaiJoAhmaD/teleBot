from telegram import Update, ChatMember
from telegram.ext import CommandHandler, ContextTypes
from telegram.constants import ParseMode

async def cek_bot_perms(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Menampilkan izin bot sendiri di grup."""
    chat = update.effective_chat
    if chat.type == "private":
        await update.message.reply_text("ℹ️ Perintah ini hanya untuk grup.")
        return True

    bot_id = context.bot.id
    try:
        member = await chat.get_member(bot_id)
    except Exception as e:
        await update.message.reply_text(f"❌ Gagal mengambil informasi bot: {e}")
        return True

    if member.status != "administrator":
        await update.message.reply_text("ℹ️ Bot bukan admin di grup ini. Hanya bisa membaca pesan yang di-mention (privacy mode).")
        return True

    # Bot adalah admin
    perms = member
    lines = [f"🤖 <b>Izin Bot</b> (@{context.bot.username})\n"]
    if perms.can_manage_chat:
        lines.append("✅ Kelola grup")
    if perms.can_delete_messages:
        lines.append("✅ Hapus pesan")
    if perms.can_manage_video_chats:
        lines.append("✅ Kelola video chat")
    if perms.can_restrict_members:
        lines.append("✅ Batasi anggota")
    if perms.can_promote_members:
        lines.append("✅ Promosikan anggota")
    if perms.can_change_info:
        lines.append("✅ Ubah info grup")
    if perms.can_invite_users:
        lines.append("✅ Undang pengguna")
    if perms.can_pin_messages:
        lines.append("✅ Sematkan pesan")
    if perms.can_manage_topics:
        lines.append("✅ Kelola topik")
    if perms.is_anonymous:
        lines.append("🕵️ Admin anonim")
    if not lines[1:]:  # tidak ada izin khusus
        lines.append("⚠️ Admin tanpa izin khusus (hanya status admin).")

    await update.message.reply_text("\n".join(lines), parse_mode=ParseMode.HTML)
    return True


async def cek_user_perms(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mengecek apakah user tertentu adalah admin dan izinnya."""
    chat = update.effective_chat
    if chat.type == "private":
        await update.message.reply_text("ℹ️ Perintah ini hanya untuk grup.")
        return True

    if not context.args:
        await update.message.reply_text("ℹ️ Gunakan: /cekuser <user_id atau @username>")
        return True

    target = context.args[0]
    # Coba resolve target jadi user ID
    try:
        if target.startswith("@"):
            # Cari berdasarkan username
            # Ini mungkin lambat, jadi bisa alternatif
            user = await context.bot.get_chat(target)  # seharusnya bisa untuk username publik
            user_id = user.id
        else:
            user_id = int(target)
    except Exception as e:
        await update.message.reply_text(f"❌ Gagal menemukan pengguna: {e}")
        return True

    try:
        member = await chat.get_member(user_id)
    except Exception as e:
        await update.message.reply_text(f"❌ Gagal mengambil info anggota: {e}")
        return True

    if member.status == "administrator":
        perms = member
        lines = [f"👤 <b>Admin:</b> {member.user.mention_html()} (`{member.user.id}`)\n"]
        if perms.can_be_edited:
            lines.append("✅ Dapat diedit oleh admin lain")
        if perms.can_manage_chat:
            lines.append("✅ Kelola grup")
        if perms.can_delete_messages:
            lines.append("✅ Hapus pesan")
        if perms.can_manage_video_chats:
            lines.append("✅ Kelola video chat")
        if perms.can_restrict_members:
            lines.append("✅ Batasi anggota")
        if perms.can_promote_members:
            lines.append("✅ Promosikan anggota")
        if perms.can_change_info:
            lines.append("✅ Ubah info grup")
        if perms.can_invite_users:
            lines.append("✅ Undang pengguna")
        if perms.can_pin_messages:
            lines.append("✅ Sematkan pesan")
        if perms.can_manage_topics:
            lines.append("✅ Kelola topik")
        if perms.is_anonymous:
            lines.append("🕵️ Admin anonim")
        if not lines[1:]:
            lines.append("⚠️ Tanpa izin khusus.")
        lines.append(f"\n📌 Status: Administrator")
        await update.message.reply_text("\n".join(lines), parse_mode=ParseMode.HTML)
    elif member.status == "creator":
        await update.message.reply_text(f"👑 {member.user.mention_html()} adalah pemilik grup.", parse_mode=ParseMode.HTML)
    else:
        await update.message.reply_text(f"ℹ️ {member.user.mention_html()} adalah anggota biasa.", parse_mode=ParseMode.HTML)

    return True


def register(app):
    app.add_handler(CommandHandler("cekbot", cek_bot_perms))
    app.add_handler(CommandHandler("cekuser", cek_user_perms))