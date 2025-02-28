import requests
from bs4 import BeautifulSoup

# def () -> dict:
#     """Get the coin rates from the TGJU website"""
#     url = 'https://www.tgju.org/coin'
#     try:
#         response = requests.get(url)
#         response.raise_for_status()
#     except requests.RequestException as e:
#         print(f"Error fetching coin rates: {e}")
#         return None

#     soup = BeautifulSoup(response.text, 'html.parser')
#     rows = soup.find_all('tr')

#     # result = {}
#     # for row in rows:
#     #     columns = row.find_all('th') + row.find_all('td')
#     #     if len(columns) < 2:
#     #         continue

#     #     title = columns[0].get_text()
#     #     price = columns[1].get_text()

#     #     try:
#     #         price_test = int(price.split(',')[0])
#     #         result[title] = price
#     #     except ValueError:
#     #         continue

#     return rows

# print(get_coin_rates())

class CurrencyRates:
    
    def __init__(self, type):
        self.type = type
        
    def fetch(self):
        if self.type == 'coin':
            url = 'https://www.tgju.org/coin'
        
        try: 
            response = requests.get(url)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"error fetching data : {e}")
            return None
        
        return response.text
    
    def sort(self, data):
        result = ''
        soup = BeautifulSoup(data, 'html.parser')
        rows = soup.find_all('tr')
        
        i = 0
        while i < len(rows):
            row = rows[i]
            columns = row.find_all('th') + row.find_all('td')
            if len(columns) < 2: 
                i += 1
                continue 
            
            title = columns[0].get_text() # column 0 and 1 are always static in this case.
            price = columns[1].get_text()
            
            try:
                price_test = int(price.split(',')[0]) 
                price += '\n' # if its a numeric price then put a single line break at the end of the line which is price
            except:
                try:
                    price_test = rows[i+1].find_all('th') + rows[i+1].find_all('td') # find out if next row of title are currency pairs
                    test = int(price_test[1].get_text().split(',')[0])
                except:
                    i += 1
                    continue
                result += '\n\n'
                price += '\n\n' # if its a string the assum that its the title and put more line breaks
                
            result += f'{title}{(50-(len(title)+len(price))) * '-'}{price}' # form the response string
            i += 1
                        
        return result
        
    def out(self):
        data = self.fetch()
        
        if data == None:
            return None
        
        return self.sort(data)
