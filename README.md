🤖 teleBot-py3

Bot Telegram modular berbasis Python 3.14+ dengan sistem plugin yang fleksibel. Bot ini mendukung berbagai fitur mulai dari intent recognition sederhana, manajemen admin bertingkat (superadmin bot vs admin grup), pencatatan grup otomatis, hingga akses shell untuk superadmin.

🧰 Teknologi
Python 3.14+
python-telegram-bot v20+
Modul standar: json, os, subprocess, asyncio, datetime, logging

⚙️ Instalasi & Menjalankan
Clone repositori ini atau salin semua file ke folder lokal.
Install Python 3.14+ (pastikan python tersedia di PATH).
Install library yang dibutuhkan:

bash
pip install python-telegram-bot

Dapatkan token bot dari @BotFather dan catat ID Telegram Anda (gunakan /id di bot setelah dijalankan pertama kali).

Edit config.json:

json
{
  "token": "TOKEN_ID",
  "owner_id": OWNER_ID,
  "admin_file": "admin.json"
}

Jalankan bot:

bash
python bot.py

Bot akan memuat semua plugin dan mulai polling.

📄 Lisensi
Proyek ini bebas digunakan dan dimodifikasi untuk keperluan pribadi maupun komersial. Tidak ada jaminan keamanan, gunakan dengan bijak.
