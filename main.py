from typing import Final
import logging
import pickle
import os
import uuid
import requests
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, InlineQueryHandler, CallbackQueryHandler, Filters, ContextTypes
from telegram.ext.dispatcher import run_async
from googletrans import Translator

TOKEN: Final = "YOUR_TELEGRAM_BOT_TOKEN"
BOT_USERNAME: Final = "@telebotpy_robot"

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Initialize pickledb for data persistence
db_path = "bot_data.db"
db = pickle.load(open(db_path, "rb")) if os.path.exists(db_path) else {}

# Initialize Google Translate API
translator = Translator()

# Commands

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام، ممنون که بهم پیام دادی!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("من یک چت بات هستم. برای استفاده از من، پیام خود را ارسال کنید!")

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("این یک دستور سفارشی است.")

async def auth_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id in db.get("authorized_users", []):
        await update.message.reply_text("شما قبلاً مجاز شده‌اید!")
    else:
        db.setdefault("authorized_users", []).append(user_id)
        pickle.dump(db, open(db_path, "wb"))
        await update.message.reply_text("شما اکنون مجاز شده‌اید!")

# Responses

def handle_response(text: str) -> str:
    processed_text = text.lower()

    if "سلام" in processed_text:
        return "علیک سلام!"

    if "حالت چطوره؟" in processed_text:
        return "ممنون، باتریم هنوز شارژ داره!"

    if "سازنده" in processed_text:
        return "سازنده‌ی من علی ماسک است!"

    if "ترجمه" in processed_text:
        return translate_text(processed_text)

    return "متوجه پیام شما نشدم. لطفا دوباره تلاش کنید."

def translate_text(text: str) -> str:
    try:
        result = translator.translate(text, dest='en')
        return f"ترجمه به انگلیسی: {result.text}"
    except Exception as e:
        logging.error(f"Error translating text: {e}")
        return "خطا در ترجمه متن!"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type = update.message.chat.type
    text = update.message.text

    if message_type == "group":
        if BOT_USERNAME in text:
            new_text = text.replace(BOT_USERNAME, "").strip()
            response = handle_response(new_text)
        else:
            return
    else:
        response = handle_response(text)

    await update.message.reply_text(response)

# Inline Queries

async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    results = [
        InlineQueryResultArticle(
            id=str(uuid.uuid4()),
            title='Response',
            input_message_content=InputTextMessageContent(handle_response(query))
        )
    ]
    await update.inline_query.answer(results)

# Callback Queries

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.message.reply_text("You pressed a button!")

# File Upload Handler

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ممنون برای ارسال فایل!")

# Error Handling

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.error(f'Update {update} caused error {context.error}')

if __name__ == "__main__":
    print("Starting Bot...")
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("custom", custom_command))
    app.add_handler(CommandHandler("auth", auth_command))

    # Message handler
    app.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Inline query handler
    app.add_handler(InlineQueryHandler(inline_query))

    # Callback query handler
    app.add_handler(CallbackQueryHandler(button_callback))

    # File upload handler
    app.add_handler(MessageHandler(Filters.document, handle_document))

    # Error handler
    app.add_error_handler(error)

    # Start polling
    print("Bot is running...")
    app.run_polling(poll_interval=5)
 