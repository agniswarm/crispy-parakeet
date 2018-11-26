from bs4 import BeautifulSoup
import urllib.request

opener = urllib.request.FancyURLopener({})
url = "https://coinmarketcap.com/all/views/all/"
f = opener.open(url)
content = f.read()
dict = {"API": "CryptoSure", "coins": {}}
soup = BeautifulSoup(content, "lxml")
for currency in soup.find_all('tr'):
    if(len(currency.select('.currency-name-container')) == 0):
        continue
    currency_name = ""
    if "..." in currency.select('.currency-name-container')[0].get_text():
        sentence = currency.select('.currency-name')[0]
        currency_name = sentence.attrs['data-sort']
    else:
        currency_name = currency.select(
            '.currency-name-container')[0].get_text()
    currency_symbol = currency.select('.col-symbol')[0].get_text()
    currency_market_cap = currency.select(
        '.market-cap')[0].get_text().replace("\n", "").replace("$", "")
    currency_price = currency.select('.price')[0].get_text().replace("$", "")
    currency_curculating_supply = currency.select(
        '.circulating-supply')[0].get_text().replace("\n", "").replace('*', "")
    currency_change = currency.select('.percent-change')
    currency_volume = currency.select('.volume')[0].get_text()
    currency_1hr_change, currency_24hrs_change, currency_7days_change = "", "", ""
    if len(currency_change) == 3:
        currency_1hr_change = currency_change[0].get_text()
        currency_24hrs_change = currency_change[1].get_text()
        currency_7days_change = currency_change[2].get_text()
    elif len(currency_change) == 2:
        currency_1hr_change = currency_change[0].get_text()
        currency_24hrs_change = currency_change[1].get_text()
    else:
        currency_1hr_change = currency_change[0].get_text()

    temp_dict = {
        "name": currency_name,
        "symbol": currency_symbol,
        "price": currency_price,
        "attr": {
            "market_cap": currency_market_cap,
            "circulating": currency_curculating_supply,
            "volume": currency_volume,
            "1hrChange": currency_1hr_change,
            "24hChange": currency_24hrs_change,
            "7daysChange": currency_7days_change
        }
    }
    dict['coins'][currency_symbol] = temp_dict
print(dict)
