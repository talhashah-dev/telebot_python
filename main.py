from typing import Final
<<<<<<< HEAD
import logging
import pickle
import os
import uuid
import requests
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, InlineQueryHandler, CallbackQueryHandler, Filters, ContextTypes
from telegram.ext.dispatcher import run_async
from googletrans import Translator
=======
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
>>>>>>> parent of f2e9c24 (add new feature)

TOKEN: Final = "6958321958:AAGiR_dlsuuFRDTl4QOKYSGS0BNWOJ0P8uQ"
BOT_USERNAME: Final = "@telebotpy_robot"

<<<<<<< HEAD
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Initialize pickledb for data persistence
db_path = "bot_data.db"
db = pickle.load(open(db_path, "rb")) if os.path.exists(db_path) else {}

# Initialize Google Translate API
translator = Translator()

=======
>>>>>>> parent of f2e9c24 (add new feature)
# Commands

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام، ممنون که بهم پیام دادی!")
    
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("من یه چت باتم، لطفا متنی تایپ کنید تا به آن پاسخ دهم!")
    
async def custome_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("این یک کماند سفارشی هست.")
    
    


async def auth_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id in db.get("authorized_users", []):
        await update.message.reply_text("شما قبلاً مجاز شده‌اید!")
    else:
        db.setdefault("authorized_users", []).append(user_id)
        pickle.dump(db, open(db_path, "wb"))
        await update.message.reply_text("شما اکنون مجاز شده‌اید!")

# Responses

def handle_reponse(text: str) -> str: 
    processed: str = text.lower()
    
    if "سلام" in processed:
        return "علیک سلام!"
        
    if "حالت چطوره؟" in processed:
        return "ممنون، باتریم هنوز شارژ داره!"
    
    if "سازندت کیه؟" in processed:
        return "علی ماسک، سازنده ی من است!"

    return "متوجه پیامتان نشدم. ربات درحال حاضر در توسعه می باشد لطفا ساعتی بعد مزاحم شوید."

<<<<<<< HEAD
    if "ترجمه" in processed_text:
        return translate_text(processed_text)

    return "متوجه پیام شما نشدم. لطفا دوباره تلاش کنید."
=======
>>>>>>> parent of f2e9c24 (add new feature)

def translate_text(text: str) -> str:
    try:
        result = translator.translate(text, dest='en')
        return f"ترجمه به انگلیسی: {result.text}"
    except Exception as e:
        logging.error(f"Error translating text: {e}")
        return "خطا در ترجمه متن!"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text
    
    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')
    
    if message_type == "group":
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, "").strip()
            response: str = handle_reponse(new_text)
        else:
            return
    else:
        response: str = handle_reponse(text)
    
    print("Bot", response)
    await update.message.reply_text(response)
<<<<<<< HEAD

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
=======
    
>>>>>>> parent of f2e9c24 (add new feature)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')
    
    
if __name__ == "__main__":
    print("Starting...")
    app = Application.builder().token(TOKEN).build()
    
    # Commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
<<<<<<< HEAD
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
 
=======
    app.add_handler(CommandHandler("custome", custome_command))
    
    # Message
    app.add_handler(MessageHandler(filters.Text, handle_message))
    
    # Errors
    app.add_error_handler(error)
    
    # Polling
    print("Polling...")
    app.run_polling(poll_interval=3)
    
>>>>>>> parent of f2e9c24 (add new feature)
