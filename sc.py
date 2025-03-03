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
        elif self.type == 'foreign-ex':
            url = 'https://www.tgju.org/currency'
        
        try: 
            response = requests.get(url)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"error fetching data : {e}")
            return None
        
        return response.text
    
    def sort(self, data):
        result = dict()
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
            
            try: # see if we have a price/title :
                price_test = int(price.split(',')[0]) 
            except: # if we have a pair of title/title then :
                try: # find out if next row of title are currency pairs :
                    title_test = rows[i+1].find_all('th') + rows[i+1].find_all('td') 
                    test = int(price_test[1].get_text().split(',')[0])
                except: # if dont go to next row
                    i += 1
                    continue
            result.update({f'{title.strip()}':f'{price.strip()}'})
            i += 1
                        
        return result
        
    def out(self):
        data = self.fetch()
        
        if data == None:
            return None
        
        return self.sort(data)
