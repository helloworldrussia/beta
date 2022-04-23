import asyncio
from binance import AsyncClient, BinanceSocketManager
from binance.enums import KLINE_INTERVAL_30MINUTE, KLINE_INTERVAL_5MINUTE


async def sock_main(name):
    client = await AsyncClient.create()
    bm = BinanceSocketManager(client)
    # start any sockets here, i.e a trade socket
    ts = bm.trade_socket(name)
    ks = bm.kline_socket(name, interval=KLINE_INTERVAL_5MINUTE)

    async with ts as tscm:
        res = await tscm.recv()
    async with ks as kscm:
        klines = await kscm.recv()

    await client.close_connection()
    return res, klines
