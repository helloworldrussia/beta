import asyncio
import threading
import time
from datetime import datetime

from binance import Client

from gd.config import b_secret, b_client
from parsers.backend import Coin
from parsers.sock import sock_main

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
coin = Coin('DOGEUSDT', client, False)
klines = coin.get_klines()
print(len(klines[:30]))
mid = coin.get_middle(klines[:30])
print(mid)
#
#
# def start_thread(coins_list):
#     i = 1
#     for coin in coins_list:
#         th = threading.Thread(target=main, args=(coin,))
#         th.start()
#         if i == 500:
#             time.sleep(60)
#         i += 1
#     return coins_list
#
#
# def set_middle_to_coin(coin):
#     klines = coin.get_klines()
#     epmpty_list = []
#     if klines == epmpty_list:
#         return 0
#     klines.remove(klines[-1])
#     l_klines = klines[-20:]
#     coin.middle = coin.get_middle(l_klines)
#
#
# def main(coin):
#     coin = Coin(coin, client, False)
#     i = 10
#     while True:
#         if i == 10:
#             set_middle_to_coin(coin)
#             i = 1
#         loop = asyncio.new_event_loop()
#         now = float(loop.run_until_complete(sock_main(coin.name))['p'])
#         if now > coin.middle:
#             res = (now - coin.middle) / coin.middle * 100
#             k = '+'
#         else:
#             k = '-'
#             res = (coin.middle - now) / coin.middle * 100
#         print(f'[{coin.name}] Разница в цене: {k}{res}%   |   {datetime.now()}')
#         time.sleep(300)
#         i += 1
#
#
# info = client.get_exchange_info()
# coins_list = []
# for x in info['symbols']:
#     coins_list.append(x['symbol'])
#
# start_thread(coins_list)
