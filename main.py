import os
import telegram
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import openai
import random
import datetime

# گرفتن کلید از محیط
openai.api_key = os.getenv("OPENAI_API_KEY")
telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
chat_id = os.getenv("CHAT_ID")

motivations = [
    "تو توانایی انجام هر کاری رو داری، فقط شروع کن.",
    "حتی اگه امروز خسته‌ای، یادت باشه که آینده رو خودت می‌سازی.",
    "هیچ‌کس مثل تو نیست؛ این یعنی قدرت تو منحصر به فرده.",
    "سکوت و تمرکز، رمز پیشرفته. ادامه بده.",
    "تو از خیلی‌ از آدمایی که شروع نکردن، جلوتری.",
    "تغییر واقعی از درون شروع میشه. به خودت ایمان داشته باش.",
    "بعضی وقتا سکوت، پرصداترین فریاده. رشد کن در سکوت.",
]

async def start(update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="سلام کسرا")

async def motivate(context):
    text = random.choice(motivations)
    await context.bot.send_message(chat_id=chat_id, text=text)

async def wake_up(context):
    await context.bot.send_message(chat_id=chat_id, text="بیدار شو")

app = ApplicationBuilder().token(telegram_token).build()

app.add_handler(CommandHandler("start", start))

# Job Queue
job_queue = app.job_queue
job_queue.run_daily(wake_up, time=datetime.time(hour=5, minute=0, second=0))
job_queue.run_repeating(motivate, interval=6*60*60, first=10)

print("ربات روشنه...")
app.run_polling()