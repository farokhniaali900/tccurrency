import requests
from bs4 import BeautifulSoup
from telegram import Bot
from telegram.ext import Application, CommandHandler

def remove_tags(t):
    return str(t).split('>')[1].split('<')[0]


def coin_rates():
    
    url = 'https://www.tgju.org/coin'

    response = requests.get(url)

    if response.status_code == 200:
        
        result = dict()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        rows = soup.find_all('tr')
        
        for row in rows:
            columns = row.find_all('th')
            columns += row.find_all('td')
            columns = list(columns)
            
            if len(columns) < 2: continue
                
            title = remove_tags(columns[0])
            price = remove_tags(columns[1])
                    
            #make sure we have a pair of price and title, if not we dont update the result with this.
            try:
                price_test = int(price.split(',')[0])
                result.update({title:price})
            except:
                continue
            
        return result
    return None


async def coin(update, context):
    
    result = "This Is a Test Request!\n\n"
    rates = coin_rates()
    
    if rates:
        
        for title, price in rates.items():
            result += f"{title}{(50-(len(title)+len(price)))*"-"}{price}\n"
            
        await update.message.reply_text(result)
        return
    await update.message.reply_text("Sorry, Couldn't fetch the data.")
    
    
def main():
    
    token = '7481362685:AAGM7Hm5ePDZo3Xy0KIGzUjK22WYpOaSkP8'

    application = Application.builder().token(token).build()
    
    application.add_handler(CommandHandler('coin', coin))
    
    application.run_polling()
    
if __name__ == '__main__':
    main()
    

