import requests
from bs4 import BeautifulSoup
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext, CallbackQueryHandler, MessageHandler
import os

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


