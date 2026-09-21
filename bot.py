import logging
import requests
import json
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes 

### Set up logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO) 

### =========================================================================

### 🛠️ আপনার কনফিগারেশন (টোকেন ও আইডি ফিক্সড)

### =========================================================================

TELEGRAM_BOT_TOKEN = "8844349499:AAEwAPVmq8FcJSuLw11ixiPUQCm6iD55s1c"
ALLOWED_USER_ID = 8523238784 

### =========================================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
if update.effective_user.id != ALLOWED_USER_ID:
return
await update.message.reply_text("👋 [Hermes Pure Live] হ্যালো! আমি চ্যানেল চেকের সব ঝামেলা চিরতরে ডিলিট করে দিয়েছি। এখন আমি সরাসরি আপনার প্রশ্নের উত্তর দেব। আমাকে যেকোনো প্রম্পট বা কোড লিখতে দিন।") 

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
if update.effective_user.id != ALLOWED_USER_ID:
return 

user_message = update.message.text
await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

# ডিরেক্ট ওপেন রাউটার ফ্রি Hermes এপিআই কল

url = "[https://openrouter.ai/api/v1/chat/completions](https://openrouter.ai/api/v1/chat/completions)"
api_key = os.environ.get("OPENROUTER_API_KEY")

if not api_key:
await update.message.reply_text("⛔ এরর: গিটহাব সেটিংসের ভেতর OPENROUTER_API_KEY খুঁজে পাওয়া যায়নি। অনুগ্রহ করে Settings -> Secrets -> Actions চেক করুন।")
return

headers = {
"Authorization": f"Bearer {api_key}",
"Content-Type": "application/json"
}

data = {
"model": "nousresearch/hermes-3-llama-3.1-405b:free",
"messages": [
{"role": "system", "content": "You are Hermes Agent, a highly capable AI assistant. You must always communicate and respond in clear, standard, and natural Bengali (প্রমিত বাংলা). Avoid robotic or literal translations from English. Use simple and universal Bengali words that are easy to understand. Keep technical keywords in English but explain context in Bengali."},
{"role": "user", "content": user_message}
]
}

try:
response = requests.post(url, headers=headers, data=json.dumps(data), timeout=60)
result = response.json()
if "choices" in result and len(result["choices"]) > 0:
    bot_response = result["choices"]["message"]["content"]
else:
    bot_response = "দুঃখিত, ওপেন রাউটার রেসপন্স ফরম্যাটে সমস্যা হয়েছে। অনুগ্রহ করে আবার চেষ্টা করুন।"

except Exception as e:
bot_response = f"যোগাযোগ করার সময় একটি ত্রুটি ঘটেছে: {str(e)}"

await update.message.reply_text(bot_response)

def main() -> None:
application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)) 

print("🤖 Telegram Bot is running perfectly without any forcing channels...")
application.run_polling(drop_pending_updates=True)
if **name** == '**main**':
main()