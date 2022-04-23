import asyncio
import random
import time
from datetime import datetime

from binance import Client

from gd.config import b_secret, b_client
from parsers.sock import sock_main


class Coin:
    def __init__(self, name, client, request_timeout):
        self.name = name
        self.client = client
        if request_timeout:
            self.client.REQUEST_TIMEOUT = request_timeout
        else:
            pass
        self.middle = None

    def b_ready(self, middle):
        while True:
            time.sleep(60)
            successful = 0
            while not successful:
                try:
                    loop = asyncio.new_event_loop()
                    a = loop.run_until_complete(sock_main(self.name))
                    successful = 1
                except:
                    time.sleep(random.randint(1, 4))
            current = a[1]['k']
            o, c = float(current['o']), float(current['c'])
            if c - o > 0:
                color = 'green'
            else:
                color = 'red'
            current_vol = float(current['v'])
            # print(self.name, middle, current_vol, color)
            if middle*2 < current_vol:
                if color == 'green':
                    break
        return f'{self.name}. {middle} < {current_vol} | {color}'

    def get_middle(self, klines):
        all = []
        for kline in klines:
            kline = self.get_status(kline)
            all.append(float(kline['c_price']))
        try:
            res = sum(all) / len(all)
        except Exception as ex:
            # print(f'in middle func {ex}\nCOIN: {self.name}\n{all} {len(all)}')
            res = None
        return res

    def get_klines(self):
        date = str(datetime.now()).split(' ')[0]
        klines = self.client.get_historical_klines(f"{self.name}", Client.KLINE_INTERVAL_5MINUTE, f"{date}")
        return klines

    def get_status(self, row):
        # if param == 'actual':
        #     row = klines[-1]
        #     one_more_row = klines[-2]
        #
        # if param == '':
        #     row = klines[-2]
        #     one_more_row = klines[-3]
        # else:
        #     row = klines[-3]
        #     one_more_row = klines[-4]

        doge_volume, usdt_volume, c_price, H, L = row[5], row[7], row[4], row[2], row[3]
        open_vs_close = float(row[1]) - float(c_price)
        if open_vs_close <= 0:
            color = 'green'
        else:
            color = 'red'
        # return klines
        return {"first_volume": doge_volume,
                "second_volume": usdt_volume,
                "o_price": row[1],
                "c_price": c_price,
                "color": color,
                "H": H,
                "L": L,
                "open_vs_close": open_vs_close}

    def purchase(self, param):
        depth = self.client.get_order_book(symbol=self.name)
        if param == 'buy':
            price = depth['asks'][0][0]
        else:
            price = depth['bids'][0][0]
        return price

    def buy(self):
        order = self.client.order_market_buy(
            symbol=self.name,
            quantity=98)
        price = order['fills'][0]['price']
        return price

    # def sell(self, price):
    #     try:
    #         order = self.client.order_limit_sell(
    #             symbol=self.name,
    #             quantity=97,
    #             price=price)
    #     except:
    #         order = self.client.order_limit_sell(
    #             symbol=self.name,
    #             quantity=96,
    #             price=price)
    #     # print(order.Id)
    #     print(f'try to SELL {price}')
    #     signal = 1
    #     i = 0
    #     while signal == 1:
    #         time.sleep(10)
    #         check = self.client.get_order(
    #             symbol=self.name,
    #             orderId=f'{order["orderId"]}')
    #         print(check['status'])
    #         if check['status'] == 'FILLED':
    #             signal = 0
    #
    # def depth(self):
    #     depth = self.client.get_order_book(symbol=self.name)
    #     asks_count, bids_count = 0, 0
    #     for x in depth['asks']:
    #         asks_count += float(x[1])
    #     for x in depth['bids']:
    #         bids_count += float(x[1])
    #     return {"продают": asks_count, "покупают": bids_count, "k": asks_count - bids_count}