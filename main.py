import requests
import json
import time
import logging
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Spread, Base
import os

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
    S = f'mysql+mysqlconnector://{os.getenv("DB_USER", "root")}:{os.getenv("DB_PASSWORD", "root")}@{os.getenv("DB_HOST", "localhost")}:{os.getenv("DB_PORT", "3306")}/{os.getenv("DB_NAME", "schema_name")}'
    print(f'Connecting to database: {S}')
    engine = create_engine(S)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Get the last row if it exists
    last_row = session.query(Spread).order_by(Spread.id.desc()).first()

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
            if last_row is not None and last_row.bid_diff == bid_diff / float(binance_best_bid) and last_row.ask_diff == ask_diff / float(okx_best_bid):
                time.sleep(100)
                continue

            ts = okx_data['data'][0]['ts']
            dt = datetime.datetime.fromtimestamp(int(ts[:-3]))

            row = Spread(
                ts=dt,
                binance_best_bid=binance_best_bid,
                binance_best_ask=binance_best_ask,
                okx_best_bid=okx_best_bid,
                okx_best_ask=okx_best_ask,
                bid_diff=bid_diff / float(binance_best_bid),
                ask_diff=ask_diff / float(okx_best_bid)
            )

            session.add(row)
            session.commit()

            last_row = session.query(Spread).order_by(Spread.id.desc()).first()

            time.sleep(100)
        except Exception as e:
            print("An error occurred:", e)
            print("Pausing script for 5 minutes...")
            time.sleep(600)

if __name__ == '__main__':
    main()