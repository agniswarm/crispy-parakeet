from flask import Flask
application = Flask(__name__)
from bs4 import BeautifulSoup
import requests
from flask import jsonify

coins = ["ETH","BTC","LTC","XRP","OMG","REQ","ZRX","GNT","BAT","AE","TRX","XLM","NEO","GAS","XRB","NCASH","EOS","CMT","ONT","ZIL","IOST","ACT","ZCO","SNT","POLY","ELF","REP","QKC","XZC","BCHABC","TUSD","BCHSV","MDA","PAX","ADA","RVN","ETC","XMR","BNB","LINK","USDC","PHX","ZEC","XEM","NEBL","CLOAK","ICX","VET","IOTA","DOCK","MFT","NANO","DASH","MITH","KEY","FUEL","WAN","WPR","RLC","AION","BCD","LSK","STEEM","DNT","GVT","NPXS","GO","BTG","WTC","VIB","QTUM","HOT","ARN","MCO","WINGS","SC","XVG","VIBE","IOTX","STORM","SNM","BQX","LUN","MTH","THETA","DENT","YOYO","MANA","LOOM","OAX","WAVES","POE","NAS","GTO","ARK","MTL","AST","DLT","RCN","STRAT","GRS","GXS","MOD","SALT","KMD","BCPT","LEND","QLC","KNC","ENJ","INS","TNB","OST","WABI","FUN","CVC","SUB","BTS","SNGLS","SYS","AMB","NULS","SKY","ENG","ADX","DATA","POWR","APPC","AGI","NXS","PPT","QSP","STORJ","POA","RDN","CND","CDT","ARDR","PIVX","DCR","BLZ","TNT","BNT","HC","LRC","ZEN","DGD","EVX","VIA","NAV","BRD","EDO"]
def refactor(input):
    return input.get_text().replace("\n", "").replace('*', "").replace(",", "").replace("$", "").replace("?","0").replace('Low Vol','0')

url = "https://coinmarketcap.com/all/views/all/"
@application.route('/')
def hello_world():
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    dict = {"API": "CryptoSure", "coins": {}}
    for currency in soup.find_all('tr'):
        currency_symbol = currency.select('.col-symbol')[0].get_text()
        if currency_symbol in coins:
            if(len(currency.select('.currency-name-container')) == 0):
                continue
            currency_name = ""
            if "..." in currency.select('.currency-name-container')[0].get_text():
                sentence = currency.select('.currency-name')[0]
                currency_name = sentence.attrs['data-sort']
            else:
                currency_name = currency.select('.currency-name-container')[0].get_text()
            currency_market_cap = float(refactor(currency.select('.market-cap')[0]))
            currency_price = float(refactor(currency.select('.price')[0]))
            currency_curculating_supply = float(refactor(currency.select('.circulating-supply')[0]))
            currency_volume = float(refactor(currency.select('.volume')[0]))/currency_price
            currency_change = currency.select('.percent-change')
            currency_1hr_change, currency_24hrs_change, currency_7days_change = 0, 0, 0
            if len(currency_change) == 3:
                currency_1hr_change = float(currency_change[0].get_text().replace("%", "").replace("?","0"))
                currency_24hrs_change = float(currency_change[1].get_text().replace("%", "").replace("?","0"))
                currency_7days_change = float(currency_change[2].get_text().replace("%", "").replace("?","0"))
            elif len(currency_change) == 2:
                currency_1hr_change = float(currency_change[0].get_text().replace("%", "").replace("?","0"))
                currency_24hrs_change = float(currency_change[1].get_text().replace("%", "").replace("?","0"))
            else:
                currency_1hr_change = float(currency_change[0].get_text().replace("%", "").replace("?","0"))

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
    return jsonify(dict)


if __name__ == '__main__':
    application.run()
