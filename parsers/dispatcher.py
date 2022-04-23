import threading
import time
from datetime import datetime

from binance import Client

from api.models import Worker
from gd.config import b_secret, b_client
from parsers.backend import Coin

"""Расшифровка ответа от метода klines
[
  [
    1499040000000,      // Open time
    "0.01634790",       // Open
    "0.80000000",       // High
    "0.01575800",       // Low
    "0.01577100",       // Close
    "148976.11427815",  // Volume
    1499644799999,      // Close time
    "2434.19055334",    // Quote asset volume
    308,                // Number of trades
    "1756.87402397",    // Taker buy base asset volume
    "28.46694368",      // Taker buy quote asset volume
    "17928899.62484339" // Ignore.
  ]
]"""

client = Client(b_client, b_secret)
name = 'DOGEUSDT'


def start_coin():
    coin = Coin(name, client, False)
    rows = coin.get_klines()[-3:]
    print(rows)
    data = []
    for row in rows:
        row = coin.get_status(row)
        data.append(row)
    try:
        worker = Worker.objects.get(name='DOGEUSDT')
    except:
        worker = Worker()
        worker.name = 'DOGEUSDT'
        worker.jobs = 0
        worker.coins = 0
    data = data[-1]
    worker.status = f'{name} Price: {data["c_price"]} First Volume: {data["first_volume"]}' \
                    f' Second Volume: {data["second_volume"]}'

    worker.save()
    return worker.status