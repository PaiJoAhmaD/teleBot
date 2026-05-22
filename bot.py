import logging
import importlib
import pkgutil
import plugins
import time
start_time = time.time()

from telegram import Update
from telegram.ext import Application, CommandHandler

import json

# ==================== KONFIGURASI ====================

# Baca konfigurasi
with open("config.json", "r") as f:
    config = json.load(f)
    
TOKEN = config["token"]
OWNER_ID = config["owner_id"]   # bisa dipakai jika perlu    

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

logging.getLogger("httpx").setLevel(logging.WARNING)

# ==================== PEMUAT PLUGIN ====================
def load_plugins(app: Application):
    for loader, module_name, is_pkg in pkgutil.iter_modules(plugins.__path__):
        if not is_pkg:
            try:
                module = importlib.import_module(f"plugins.{module_name}")
                if hasattr(module, "register"):
                    module.register(app)
                    logger.info(f"✅ Plugin '{module_name}' dimuat.")
                else:
                    logger.warning(f"⚠️ Plugin '{module_name}' tidak memiliki register().")
            except Exception as e:
                logger.error(f"❌ Gagal memuat plugin '{module_name}': {e}")

# ==================== MAIN ====================
def main():
    if TOKEN == "TOKEN":
        logger.critical("Token belum diisi!")
        return

    app = Application.builder().token(TOKEN).build()

    # Command dasar (opsional, bisa juga di plugin)
    async def start(update, context):
        await update.message.reply_text("Bot siap! Gunakan fitur yang tersedia.")
    app.add_handler(CommandHandler("start", start))

    # Muat semua plugin (termasuk fallback)
    load_plugins(app)

    logger.info("Bot berjalan...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
