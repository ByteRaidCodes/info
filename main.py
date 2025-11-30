import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
RAPID_API_KEY = os.getenv("RAPID_API_KEY")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send any Instagram username 👇")

async def get_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.text.replace("@", "").strip()

    url = f"https://instagram-scraper-20251.p.rapidapi.com/userinfo/{username}"

    headers = {
        "x-rapidapi-key": RAPID_API_KEY,
        "x-rapidapi-host": "instagram-scraper-20251.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers).json()

    if "error" in response:
        await update.message.reply_text("⚠ User not found or Private account.")
        return

    data = response["data"]

    msg = f"""
📌 Instagram Profile Info

👤 Name: {data.get('full_name')}
🔖 Username: @{data.get('username')}
✔ Verified: {data.get('is_verified')}
🔒 Private: {data.get('is_private')}
🏪 Business: {data.get('is_business')}
📜 Bio: {data.get('biography')}
🔗 URL: {data.get('external_url')}
👥 Followers: {data.get('followers')}
➡ Following: {data.get('following')}
🖼 Posts: {data.get('posts')}
"""

    await update.message.reply_text(msg, parse_mode="Markdown")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_info))
app.run_polling()
