import os
from time import time
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from sc import CurrencyRates

async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [KeyboardButton("قیمت سکه 🪙")],
        [KeyboardButton("نرخ ارز ها 💶")],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)

    await update.message.reply_text(
        "Main Menu:",
        reply_markup=reply_markup
    )
    
# Function to send the start message
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [KeyboardButton("خانه 𖧝")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
    
    await update.message.reply_text(
        "welcome!",
        reply_markup=reply_markup,
    )
    
async def currency_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, currency_type):
    global get_rates, rates, fetched_at
    global current_currency_type
    
    current_currency_type = currency_type
    get_rates = CurrencyRates(currency_type)
    rates = get_rates.out()
    
    fetched_at = time()
    
    keyboard = [
        [KeyboardButton("خانه 𖧝")],
    ]
    
    for title in rates.keys():
        keyboard.append([KeyboardButton(f'{title}')])
        
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
    
    message = "🪙 لطفاً نوع سکه مورد نظر خود را انتخاب کنید:" if currency_type == 'coin' else \
        "💶 لطفاً نوع ارز مورد نظر خود را انتخاب کنید:"

    
    await update.message.reply_text(
        message,
        reply_markup=reply_markup
    )

# Function to handle button clicks (reply keyboard works with text input)
async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_text = update.message.text  # User's selected button text
    
    if user_text == "خانه 𖧝":
        await main_menu(update, context)
    elif user_text == "قیمت سکه 🪙":
        await currency_menu(update, context, "coin")
    elif user_text == "نرخ ارز ها 💶":
        await currency_menu(update, context, "foreign-ex")
    else:
        try:
            if (time() - fetched_at) > 30:
                rates = get_rates.out()
            if current_currency_type == 'coin':
                await update.message.reply_text(
                    f''' 
🪙 قیمت لحظه‌ای سکه:  
{user_text} : {rates[user_text]} تومان  

📊 برای دریافت قیمت سایر سکه‌ها، گزینه موردنظر را انتخاب کنید.  
🔄 به‌روزرسانی خودکار | دقیق و سریع 
                    '''
                )
            elif current_currency_type == 'foreign-ex':
                await update.message.reply_text(
                    f''' 
💶 قیمت لحظه‌ای ارزها:  
{user_text} : {rates[user_text]} تومان  

📊 برای دریافت قیمت سایر سکه‌ها، گزینه موردنظر را انتخاب کنید.  
🔄 به‌روزرسانی خودکار | دقیق و سریع 
                    '''
                )
        except:
            await update.message.reply_text("Please select a valid option.")

# Main function to start the bot
def main():
    #TOKEN = os.environ.get('BOT_TOKEN')
    BOT_TOKEN = os.environ.get('BOT_TOKEN')
    
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_buttons))
    
    app.run_polling()

if __name__ == '__main__':
    main()
