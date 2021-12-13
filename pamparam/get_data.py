import config
import threading
import time
from binance.client import Client
from tafunc import ta_analyze
from collections import OrderedDict
# @todo: add overload for user selection of data intervals
# this function gets the kline data provided in the binance api


def get_klines(selected_interval):
    client = Client(config.API_KEY, config.API_SECRET)

    # get the possible exchanges for the quoting asset, that are spot tradeable
    exinfo = client.get_exchange_info()
    exlist = []

    for symbol in exinfo["symbols"]:
        if((symbol["quoteAsset"] == "USDT")
            & (symbol["isSpotTradingAllowed"] is True)):
            exlist.append(symbol["symbol"])

    # getting the kline data to analyse for the exchangeable assets
    klines = {}
    unsorted = {}
    if selected_interval == "1HOUR":
        s_interval = Client.KLINE_INTERVAL_1HOUR
    elif selected_interval == "15MIN":
        s_interval = Client.KLINE_INTERVAL_15MINUTE
    elif selected_interval == "4HOUR":
        s_interval = Client.KLINE_INTERVAL_4HOUR
    elif selected_interval == "1DAY":
        s_interval = Client.KLINE_INTERVAL_1DAY
    elif selected_interval == "1MIN":
        s_interval = Client.KLINE_INTERVAL_1MINUTE
    else:
        s_interval = Client.KLINE_INTERVAL_4HOUR

    # @todo:multithreading here, done

    threadLock = threading.Lock()
    threads = []
    i = 0
    for exchange in exlist:
        # candledata = []#one of my ultimate bruh moments,
        # it shall remain here as a memento mori
        try:
            print(exchange)
            new_thread = threading.Thread(target=apicall_thread, args=(
                client, exchange, s_interval, unsorted, klines, threadLock))
            new_thread.start()
            threads.append(new_thread)
            i = i + 1
            # not bruh moments
            # candledata = (client.get_klines(*yadayada*))
            # klines[exchange] = candledata
            # unsorted[exchange] = ta_analyze(candledata)
        except Exception as e:
            print("can't because")
            print(e)

    for t in threads:
        t.join()

    # sorting with lambda black magic fuckery
    sortedsigs = dict(OrderedDict(
        sorted(unsorted.items(), key=lambda t: t[1]['signal'])))
    print(str(i) + " coins analysed and sorted")

    return (sortedsigs)


def get_one_kline():  # trial method for getting kline data
    client = Client(config.API_KEY, config.API_SECRET)

    try:
        a = (client.get_klines(symbol="DOGEUSDT",
                               interval=Client.KLINE_INTERVAL_15MINUTE,
                               limit=1))

        dct = dict(zip(range(12), a))
        return dct

    except Exception as e:
        print(e)
        return("nah")


def apicall_thread(client, exchange, s_interval, unsorted, klines, lock):
    # parellelized part
    candledata = (client.get_klines(
        symbol=exchange, interval=s_interval, limit=50))
    ta_result = ta_analyze(candledata)
    # mutex
    lock.acquire()
    klines[exchange] = candledata
    unsorted[exchange] = ta_result
    lock.release()
