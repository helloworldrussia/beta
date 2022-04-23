import threading
import time
from datetime import datetime

from binance import Client

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


def start_thread(coins_list):
    i = 1
    for coin in coins_list:
        if i == 200:
            print('Запущено 200 потокov. Пауза.')
            break
        th = threading.Thread(target=main, args=(coin,))
        th.start()
        i += 1
        coins_list.remove(coin)
    return coins_list


def main(coin):
    coin = Coin(coin, client, False)
    klines = coin.get_klines()[-36:]
    middle = coin.get_middle(klines)
    if not middle:
        return None
    message = coin.b_ready(middle)
    # print(message)


info = client.get_exchange_info()
coins_list = []
i = 1
for x in info['symbols']:
    coins_list.append(x['symbol'])
    i += 1

print('Обнаружено пар: ', len(coins_list))
coins_list = start_thread(coins_list)
start_thread(coins_list)

i = 1
while True:
    print('Active count:', threading.active_count())
    time.sleep(61)
    empty = []
    if coins_list != empty:
        coins_list = start_thread(coins_list)

# coin = Coin(coin, client, False)
# klines = coin.get_klines()[-36:]
# res = coin.get_middle(klines)
# print(coin.name, res, len(klines))


# threading.active_count()
# print(coin.get_status(klines[-1]))
# print('CURRENT:', coin.name, "\nKLINES:", len(klines))
