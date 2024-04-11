from typing import Final
import logging
import pickle
import random
import requests
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, InlineQueryHandler, CallbackQueryHandler, Filters, ContextTypes

TOKEN: Final = "YOUR_TELEGRAM_BOT_TOKEN"
BOT_USERNAME: Final = "@telebotpy_robot"

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Initialize pickledb for data persistence
db = pickle.load(open("bot_data.db", "rb")) if "bot_data.db" in os.listdir() else pickle.dumps({})

# Commands

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام، ممنون که بهم پیام دادی!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("من یک چت بات هستم. برای استفاده از من، پیام خود را ارسال کنید!")

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("این یک دستور سفارشی است.")

# Responses

def handle_response(text: str) -> str:
    processed_text = text.lower()

    if "سلام" in processed_text:
        return "علیک سلام!"

    if "حالت چطوره؟" in processed_text:
        return "ممنون، باتریم هنوز شارژ داره!"

    if "سازنده" in processed_text:
        return "سازنده‌ی من علی ماسک است!"

    return "متوجه پیام شما نشدم. لطفا دوباره تلاش کنید."

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
            id=str(uuid4()),
            title='Response',
            input_message_content=InputTextMessageContent(handle_response(query))
        )
    ]
    await update.inline_query.answer(results)

# Callback Queries

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.message.reply_text("You pressed a button!")

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

    # Message handler
    app.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Inline query handler
    app.add_handler(InlineQueryHandler(inline_query))

    # Callback query handler
    app.add_handler(CallbackQueryHandler(button_callback))

    # Error handler
    app.add_error_handler(error)

    # Start polling
    print("Bot is running...")
    app.run_polling(poll_interval=5)
