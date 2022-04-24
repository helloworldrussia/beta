import threading
import time
from datetime import datetime

from binance import Client

from api.models import Worker, Deal
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


def get_model():
    try:
        worker = Worker.object.get(name=name)
    except:
        worker = Worker()
        worker.name = name
        worker.save()
        worker = Worker.object.get(name=name)

    return worker


async def demo(object):
    deal = Deal()
    now = object.get_klines()[-1]
    now = object.get_status(now)
    buy_price = now['c_price']
    time_now = datetime.now().strftime('%H:%M %m-%d')
    buy_message = f'Момент. Цена: {buy_price} [{time_now}]'
    while True:
        now = object.get_klines()[-1]
        now = object.get_status(now)
        now = now['c_price']
        time_now = datetime.now().strftime('%H:%M %m-%d')
        if float(now)-float(buy_price) >= 0.0004:
            deal.begin = f'Момент Продажи. Цена: {now} [{time_now}]'
            deal.save()
            worker = get_model()
            worker.deals.add(deal)
            worker.save()
            return False


def check_color(data):
    successful = 0
    i = 1
    for x in data:
        if i != len(data):
            if x['color'] == "red":
                x['successful'] = 1
            else:
                x['successful'] = 0
        else:
            if x['color'] == "green":
                x['successful'] = 1
            else:
                x['successful'] = 0
        i += 1
    return data


def check_successful(data):
    successful = 0
    for row in data:
        if row['successful'] == 1:
            successful += 1
        print(row['successful'])
    if successful == len(data):
        return True
    else:
        return False


def main(coin):
    while True:
        klines = coin.get_klines()[-3:]
        rows = []
        for kline in klines:
            res = coin.get_status(kline)
            rows.append(res)
        rows = check_color(rows)
        if check_successful(rows):
            demo(coin)
        # time.sleep(300)


def start_coin():
    coin = Coin(name, client, False)
    rows = coin.get_klines()[-3:]
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
    th = threading.Thread(target=main, args=(coin,))
    th.start()
    return worker.status