import requests
from bs4 import BeautifulSoup
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext, CallbackQueryHandler, MessageHandler
import os

# Load the Telegram bot token from an environment variable
#TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
TOKEN = '7481362685:AAGM7Hm5ePDZo3Xy0KIGzUjK22WYpOaSkP8'

def get_coin_rates() -> dict:
    """Get the coin rates from the TGJU website"""
    url = 'https://www.tgju.org/coin'
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching coin rates: {e}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    rows = soup.find_all('tr')

    result = {}
    for row in rows:
        columns = row.find_all('th') + row.find_all('td')
        if len(columns) < 2:
            continue

        title = columns[0].get_text()
        price = columns[1].get_text()

        try:
            price_test = int(price.split(',')[0])
            result[title] = price
        except ValueError:
            continue

    return result

async def option(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton('مشاهده قیمت سکه', callback_data='coin')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.message:
        await update.message.reply_text("لطفا یک گزینه را انتخاب کنید.", reply_markup=reply_markup)

async def start(update: Update, context: CallbackContext) -> None:
    """Handle the /start command"""
    await update.message.reply_text("خوش آمدید")
    await option(update, context)

async def button_click(update: Update, context: CallbackContext) -> None:
    """Handle button clicks"""
    back_button = [
        [InlineKeyboardButton('بازگشت', callback_data='back')]
    ]
    reply_markup = InlineKeyboardMarkup(back_button)
    
    query = update.callback_query
    await query.answer()

    if query.data == "coin":
        result = "This Is a Test Request!\n\n"
        rates = get_coin_rates()
        if rates:
            for title, price in rates.items():
                result += f"{title}{(50-(len(title)+len(price)))*'-'}{price}\n"
            try:
                await query.edit_message_text(result, reply_markup=reply_markup)
            except Exception as e:
                print(f"Error editing message text: {e}")
        else:
            try:
                await query.edit_message_text("Sorry, Couldn't fetch the data.")
            except Exception as e:
                print(f"Error editing message text: {e}")
    elif query.data == "back":
        keyboard = [
            [InlineKeyboardButton('مشاهده قیمت سکه', callback_data='coin')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        try:
            await query.edit_message_text("لطفا یک گزینه را انتخاب کنید.", reply_markup=reply_markup)
        except Exception as e:
            print(f"Error editing message text: {e}")


def main():
    """Main function"""
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button_click))
    application.run_polling()

if __name__ == '__main__':
    main()
