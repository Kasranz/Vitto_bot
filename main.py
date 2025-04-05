
import telebot
import requests
import random
import threading
import time
from datetime import datetime
import schedule

# توکن‌ها
TELEGRAM_TOKEN = '7324379761:AAGIXWgWhUyRbT31xS6RUn94nUPYZAPXz9s'
OPENAI_API_KEY = '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'

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# پیام‌های انگیزشی برای تیپ INFJ
motivations = [
    "تو می‌تونی دنیا رو تغییر بدی، فقط با ایمان به خودت شروع کن.",
    "یادت نره که سکوتت گاهی بلندترین فریاده.",
    "تو برای چیزهای بزرگ‌تری ساخته شدی. ادامه بده.",
    "حتی اگه تنها باشی، راه درست رو برو. تو رهبر خودتی.",
    "روحت قویه، فقط گاهی دلتنگ می‌شه. ادامه بده رفیق."
]

# پیام ۵ صبح
def morning_message():
    bot.send_message(CHAT_ID, "بیدار شو! وقتشه بدرخشی.")

# پیام انگیزشی رندوم
def send_random_motivation():
    bot.send_message(CHAT_ID, random.choice(motivations))

# پاسخ با ChatGPT
def ask_chatgpt(message):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": message}]
    }
    response = requests.post(url, headers=headers, json=data)
    if response.ok:
        return response.json()['choices'][0]['message']['content']
    else:
        return "یه مشکلی پیش اومد، دوباره بپرس."

# وقتی /start زده میشه
@bot.message_handler(commands=['start'])
def start_message(message):
    global CHAT_ID
    CHAT_ID = message.chat.id
    bot.send_message(message.chat.id, "سلام کسرا")

# وقتی پیام معمولی فرستاده میشه
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    response = ask_chatgpt(message.text)
    bot.send_message(message.chat.id, response)

# برنامه‌ریزی ارسال‌ها
def schedule_jobs():
    schedule.every().day.at("05:00").do(morning_message)
    schedule.every().day.at("10:00").do(send_random_motivation)
    schedule.every().day.at("16:00").do(send_random_motivation)
    schedule.every().day.at("22:00").do(send_random_motivation)
    while True:
        schedule.run_pending()
        time.sleep(30)

# اجرا در ترد جدا
threading.Thread(target=schedule_jobs).start()

# اجرای ربات
bot.infinity_polling()
