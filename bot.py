import os
import telebot
import httpx
from PIL import Image, ImageDraw, ImageFont
from flask import Flask
from threading import Thread

# --- কনফিগারেশন ---
BOT_TOKEN = "8307147474:AAE5nmPsEMf7FFXtkxClhFiS5uWOn_rnLgo" # এখানে আপনার টোকেন দিন
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# Koyeb-এর জন্য হেলথ চেক রুট
@app.route('/')
def index():
    return "Bot is running 24/7"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

# --- আপনার SheerID লজিক ---
def process_verification(url, chat_id):
    bot.send_message(chat_id, "🔍 Verification শুরু হচ্ছে... দয়া করে অপেক্ষা করুন।")
    try:
        # এখানে আপনার আগের কোডের SheerID প্রসেসগুলো থাকবে
        # উদাহরণস্বরূপ:
        success_msg = f"🚀 **Google One Verified!**\n\nLink: {url}\nStatus: Student Premium Active"
        bot.send_message(chat_id, success_msg, parse_mode="Markdown")
    except Exception as e:
        bot.send_message(chat_id, f"❌ ভুল হয়েছে: {str(e)}")

# টেলিগ্রাম কমান্ড হ্যান্ডলার
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "স্বাগতম! ভেরিফাই করতে লিখুন: /verify YOUR_URL")

@bot.message_handler(commands=['verify'])
def verify_command(message):
    text = message.text.split()
    if len(text) < 2:
        bot.reply_to(message, "অনুগ্রহ করে URL দিন। উদাহরণ: `/verify https://link.com`", parse_mode="Markdown")
        return
    
    url = text[1]
    # একটি নতুন থ্রেডে প্রসেস শুরু করা যাতে বট হ্যাং না হয়
    Thread(target=process_verification, args=(url, message.chat.id)).start()

# বট এবং ফ্ল্যাস্ক সার্ভার একসাথে চালু করা
if __name__ == "__main__":
    print("Bot is starting...")
    # ফ্ল্যাস্ক সার্ভার আলাদা থ্রেডে চালানো (Koyeb-এর জন্য জরুরি)
    t = Thread(target=run_flask)
    t.start()
    # বট পোলিং শুরু
    bot.infinity_polling()
