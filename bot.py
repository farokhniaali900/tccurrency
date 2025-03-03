import os
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from sc import CurrencyRates

# Function to send the start message with persistent buttons
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [KeyboardButton("قیمت سکه")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)

    await update.message.reply_text(
        "Welcome to the Currency Bot! Choose an option below:",
        reply_markup=reply_markup
    )

# Function to handle button clicks (reply keyboard works with text input)
async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_text = update.message.text  # User's selected button text
    
    if user_text == "قیمت سکه":
        rates = CurrencyRates(user_text).out()
        await update.message.reply_text(rates)
    else:
        await update.message.reply_text("Please select a valid option.")

# Main function to start the bot
def main():
    TOKEN = os.environ.get('BOT_TOKEN')
    
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_buttons))
    
    app.run_polling()

if __name__ == '__main__':
    main()
