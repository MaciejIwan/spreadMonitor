import requests
import json
import time
import sqlite3
import logging
import datetime

# https://www.coingecko.com/en/coins/tether-gold
# https://www.coingecko.com/en/coins/pax-gold

logging.basicConfig(filename='my_log_file.txt', level=logging.WARNING)
logging.debug('App started')

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
    conn = sqlite3.connect('my_database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS data
                 (ts DATETIME, binance_best_bid real, binance_best_ask real, okx_best_bid real, okx_best_ask real, bid_diff real, ask_diff real)''')

    while True:
        binance_data, okx_data = get_both_data()

        binance_best_bid = binance_data['bids'][0][0]
        binance_best_ask = binance_data['asks'][0][0]
        okx_best_bid = okx_data['data'][0]['bids'][0][0]
        okx_best_ask = okx_data['data'][0]['asks'][0][0]

        bid_diff = abs(float(binance_best_bid) - float(okx_best_ask))
        ask_diff = abs(float(binance_best_ask) - float(okx_best_bid))

        ts = okx_data['data'][0]['ts']
        dt = datetime.datetime.fromtimestamp(int(ts[:-3]))

        row = (dt, binance_best_bid, binance_best_ask, okx_best_bid, okx_best_ask, bid_diff / float(binance_best_bid),
               ask_diff / float(okx_best_bid))

        c.execute("INSERT INTO data VALUES (?, ?, ?, ?, ?, ?, ?)", row)
        conn.commit()

        time.sleep(60)

    conn.close()


if __name__ == '__main__':
    main()