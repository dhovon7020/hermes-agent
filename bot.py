import logging
import requests
import json
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# =========================================================================
# 🛠️ আপনার টেলিগ্রাম এবং ওপেন রাউটার কনফিগারেশন (সম্পূর্ণ রেডি)
# =========================================================================
TELEGRAM_BOT_TOKEN = "8844349499:AAEwAPVmq8FcJSuLw11ixiPUQCm6iD55s1c"
ALLOWED_USER_ID = 8523238784
# =========================================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id != ALLOWED_USER_ID:
        return
    await update.message.reply_text("👋 [Hermes Direct Live] হ্যালো! আমি সরাসরি ওপেন রাউটারের ফ্রি Hermes মডেলে কানেক্ট হয়ে লাইভ হয়েছি। আমাকে যেকোনো প্রশ্ন বা কোডিংয়ের কাজ দিন।")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id != ALLOWED_USER_ID:
        return
        
    user_message = update.message.text
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    # ডিরেক্ট ওপেন রাউটার ফ্রি Hermes এপিআই কল (কোনো CLI বা ফাইল লাগবে না)
    url = "https://openrouter.ai"
    headers = {
        "Authorization": "Bearer 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", # আপনার ফ্রি এপিআই কি ফিক্সড করা হয়েছে
        "Content-Type": "application/json"
    }
    data = {
        "model": "nousresearch/hermes-3-llama-3.1-405b:free", # অফিশিয়াল Hermes 3 ফ্রি শক্তিশালী মডেল
        "messages": [
            {"role": "system", "content": "You are Hermes Agent. You must always respond in natural and clear Bengali language."},
            {"role": "user", "content": user_message}
        ]
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data), timeout=60)
        result = response.json()
        
        if "choices" in result and len(result["choices"]) > 0:
            bot_response = result["choices"][0]["message"]["content"]
        else:
            bot_response = "দুঃখিত, এই মুহূর্তে উত্তর জেনারেট করা যায়নি। অনুগ্রহ করে আবার চেষ্টা করুন।"
    except Exception as e:
        bot_response = f"যোগাযোগ করার সময় একটি ত্রুটি ঘটেছে: {str(e)}"
        
    await update.message.reply_text(bot_response)

def main() -> None:
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("🤖 Telegram Bot is running perfectly without any CLI dependencies...")
    application.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
