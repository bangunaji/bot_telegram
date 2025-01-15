from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import requests

# Fungsi untuk mengambil lelucon teks acak
def get_text_joke():
    url = "https://candaan-api.vercel.app/api/text/random"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get("data")
        else:
            return "Wah, API-nya lagi error nih! Coba lagi nanti ya~"
    except Exception as e:
        return f"Oops, ada masalah: {e}"

# Fungsi untuk mengambil lelucon gambar acak
def get_image_joke():
    url = "https://candaan-api.vercel.app/api/image/random"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json().get("data")
            # Validasi URL gambar
            if "url" in data and data["url"].startswith("http"):
                return data["url"], data.get("source", "Tidak ada sumber")
            else:
                return None, "Gambar tidak valid dari API."
        else:
            return None, "Wah, API-nya lagi error nih! Coba lagi nanti ya~"
    except Exception as e:
        return None, f"Oops, ada masalah: {e}"

# Command untuk menampilkan lelucon teks
async def text_joke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    joke = get_text_joke()
    await update.message.reply_text(joke)

# Command untuk menampilkan lelucon gambar
async def image_joke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    joke_url, source = get_image_joke()
    if joke_url:
        try:
            await update.message.reply_photo(photo=joke_url, caption=f"Sumber: {source}")
        except Exception as e:
            await update.message.reply_text(f"Error saat mengirim gambar: {e}")
    else:
        await update.message.reply_text(source)

# Command untuk memulai bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hai! Aku bot candaan. Gunakan perintah berikut untuk mulai bercanda:\n"
        "/text - Untuk lelucon teks\n"
        "/image - Untuk lelucon gambar\n"
        "Yuk, kita bercanda biar harimu lebih seru!"
    )

# Fungsi utama untuk menjalankan bot
def main():
    # Ganti TOKEN dengan token bot yang diberikan oleh BotFather
    TOKEN = "8148411203:AAH1SO_C5phlEtkUz_POXsANs-8xZyA-DOU"
    
    # Inisialisasi aplikasi
    application = Application.builder().token(TOKEN).build()

    # Tambahkan handler untuk perintah
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("text", text_joke))
    application.add_handler(CommandHandler("image", image_joke))

    # Jalankan bot
    print("Bot berjalan... Tekan Ctrl+C untuk berhenti.")
    application.run_polling()

if __name__ == "__main__":
    main()
