from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN: Final = "6958321958:AAGiR_dlsuuFRDTl4QOKYSGS0BNWOJ0P8uQ"
BOT_USERNAME: Final = "@telebotpy_robot"

# Commands

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام، ممنون که بهم پیام دادی!")
    
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("من یه چت باتم، لطفا متنی تایپ کنید تا به آن پاسخ دهم!")
    
async def custome_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("این یک کماند سفارشی هست.")
    
    


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
    

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')
    
    
if __name__ == "__main__":
    print("Starting...")
    app = Application.builder().token(TOKEN).build()
    
    # Commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("custome", custome_command))
    
    # Message
    app.add_handler(MessageHandler(filters.Text, handle_message))
    
    # Errors
    app.add_error_handler(error)
    
    # Polling
    print("Polling...")
    app.run_polling(poll_interval=3)
    