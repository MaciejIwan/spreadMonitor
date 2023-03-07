import requests
import json
import time

import logging

# Create a logging object
logging.basicConfig(filename='my_log_file.txt', level=logging.WARNING)

# Generate some warnings and errors
logging.debug('This is a debug message')
logging.info('This is an info message')
logging.warning('This is a warning message')
logging.error('This is an error message')
logging.critical('This is a critical message')

# https://www.coingecko.com/en/coins/tether-gold
# https://www.coingecko.com/en/coins/pax-gold

url_binance = 'https://api.binance.com/api/v3/depth'
url_okx = 'https://www.okex.com/api/v5/market/books'


def get_data(params, url):
    response = requests.get(url, params=params)
    return json.loads(response.text)


def get_both_data():
    params = {
        'symbol': 'PAXGUSDT',
        'limit': 1  # Number of bids/asks to retrieve (max 1000)
    }
    binance_data = get_data(params, url_binance)
    params = {
        'instId': 'XAUT-USDT',
        'sz': 1,  # Number of bids/asks to retrieve (max 200)
        'side': 0  # 1 for bids, 2 for asks
    }
    okx_data = get_data(params, url_okx)
    return binance_data, okx_data


def main():
    while True:
        binance_data, okx_data = get_both_data()
        with open("filename.csv", 'a+') as f:
            binance_best_bid = binance_data['bids'][0][0]
            binance_best_ask = binance_data['asks'][0][0]
            okx_best_bid = okx_data['data'][0]['bids'][0][0]
            okx_best_ask = okx_data['data'][0]['asks'][0][0]

            bid_diff = abs(float(binance_best_bid) - float(okx_best_ask))
            ask_diff = abs(float(binance_best_ask) - float(okx_best_bid))

            row = f"{okx_data['data'][0]['ts']},{binance_best_bid},{binance_best_ask},{okx_best_bid},{okx_best_ask},{bid_diff / float(binance_best_bid):.5f},{ask_diff / float(okx_best_bid):.5f}\n"
            f.write(row)
        time.sleep(80)



main()
