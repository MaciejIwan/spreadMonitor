import requests
import json
import time
import sqlite3
import logging
import datetime

# https://www.coingecko.com/en/coins/tether-gold
# https://www.coingecko.com/en/coins/pax-gold

logging.basicConfig(filename='logs/my_log_file.txt', level=logging.WARNING)
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
    conn = sqlite3.connect('resources/my_database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS data
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, ts DATETIME, binance_best_bid real, binance_best_ask real, okx_best_bid real, okx_best_ask real, bid_diff real, ask_diff real)''')

    # Get the last row if it exists
    c.execute("SELECT * FROM data ORDER BY id DESC LIMIT 1")
    last_row = c.fetchone()

    while True:
        try:
            binance_data, okx_data = get_both_data()

            binance_best_bid = binance_data['bids'][0][0]
            binance_best_ask = binance_data['asks'][0][0]
            okx_best_bid = okx_data['data'][0]['bids'][0][0]
            okx_best_ask = okx_data['data'][0]['asks'][0][0]

            bid_diff = abs(float(binance_best_bid) - float(okx_best_ask))
            ask_diff = abs(float(binance_best_ask) - float(okx_best_bid))

            # Compare bid_diff and ask_diff with the last row if it exists
            if last_row is not None and last_row[6] == bid_diff / float(binance_best_bid) and last_row[
                7] == ask_diff / float(okx_best_bid):
                print('Skipping duplicate row...')
                continue

            ts = okx_data['data'][0]['ts']
            dt = datetime.datetime.fromtimestamp(int(ts[:-3]))

            row = (
                dt, binance_best_bid, binance_best_ask, okx_best_bid, okx_best_ask, bid_diff / float(binance_best_bid),
                ask_diff / float(okx_best_bid))

            c.execute(
                "INSERT INTO data(ts, binance_best_bid, binance_best_ask, okx_best_bid, okx_best_ask, bid_diff, ask_diff) VALUES (?, ?, ?, ?, ?, ?, ?)",
                row)
            conn.commit()

            last_row = c.execute("SELECT * FROM data ORDER BY id DESC LIMIT 1").fetchone()

            time.sleep(100)
        except Exception as e:
            print("An error occurred:", e)
            print("Pausing script for 5 minutes...")
            time.sleep(600)

    conn.close()


if __name__ == '__main__':
    main()
