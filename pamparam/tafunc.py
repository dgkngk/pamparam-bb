import pandas as pd
import ta
import time
import requests
import config
from coinmetrics.api_client import CoinMetricsClient


def get_current_exchange_info(exchange, resp):
    json = resp.json()
    # print(json['data'])
    if json['success'] is True:
        for ex in json['data']:
            if ex['s'] == exchange:
                return ex
        raise Exception("not found")
    else:
        raise Exception("can't connect")


# maybe modulizing this part may help more
# @to-do: de-complexifying needed
def ta_analyze(candledata, interval, exchange, gcei_resp):

    result = {}
    last_h = float(candledata[-1][2])
    last_l = float(candledata[-1][3])
    close_list = []
    high_list = []
    low_list = []
    volume_list = []

    for trade in candledata:
        close_list.append(float(trade[4]))
        high_list.append(float(trade[2]))
        low_list.append(float(trade[3]))
        volume_list.append(float(trade[5]))

    t_c = pd.Series(close_list)
    t_high = pd.Series(high_list)
    t_low = pd.Series(low_list)
    t_vol = pd.Series(volume_list)

    t_d = ta.momentum.stochrsi_d(t_c,
                                 window=14,
                                 smooth1=3,
                                 smooth2=3,
                                 fillna=False)
    t_k = ta.momentum.stochrsi_k(t_c,
                                 window=14,
                                 smooth1=3,
                                 smooth2=3,
                                 fillna=False)
    indicator_bb = ta.volatility.BollingerBands(close=t_c,
                                                window=20,
                                                window_dev=2)
    t_bh = indicator_bb.bollinger_hband()
    t_bl = indicator_bb.bollinger_lband()
    t_bm = indicator_bb.bollinger_pband()

    t_vwap = ta.volume.volume_weighted_average_price(high=t_high,
                                                     low=t_low,
                                                     close=t_c,
                                                     volume=t_vol,
                                                     window=14)
    t_macd_s = ta.trend.macd_signal(t_c,
                                    window_slow=26,
                                    window_fast=12,
                                    window_sign=9)
    t_macd = ta.trend.macd(
        t_c,
        window_slow=26,
        window_fast=12,
    )
    t_nvt = nvt_analysis(exchange, gcei_resp)
    """
    print(t_c[len(t_c) - 1], ":", t_d[len(t_d) - 1], t_k[len(t_k) - 1],
          t_bh[len(t_bh) - 1], t_bl[len(t_bl) - 1], t_vwap[len(t_vwap) - 1],
          t_macd_s[len(t_macd_s) - 1], t_macd[len(t_macd) - 1])"""


    overpriced = 0
    underpriced = 0
    bull = 0
    bear = 0

    result_k = float("{0:.2f}".format(t_k[len(t_k) - 1] * 100))
    result_d = float("{0:.2f}".format(t_d[len(t_d) - 1] * 100))
    result_close = t_c[len(t_c) - 1]
    result_bbh = t_bh[len(t_bh) - 1]
    result_bbm = t_bm[len(t_bm) - 1]
    result_bbl = t_bl[len(t_bl) - 1]
    result_vwap = float("{0:.3f}".format(t_vwap[len(t_vwap) - 1]))
    result_macd = float("{0:.3f}".format(t_macd[len(t_macd) - 1]))
    result_macd_s = float("{0:.3f}".format(t_macd_s[len(t_macd_s) - 1]))

    # half of the standard deviation
    proximity_factor = abs(
        (result_bbh - result_bbm) / 4)

    # NaN is not equal to itself
    if result_k != result_k or result_vwap != result_vwap:
        raise ValueError(
            """DO NOT PANIC,
can't analyze this coin because there is not enough data.
Maybe it's a newly issued coin?""")

    # NVT signal
    if (t_nvt == -999):
        result["NVT"] = "NO NVT"
    else:
        result["NVT"] = t_nvt

    # StochRSI
    # some hacking to clear out unnecessary precision
    result["SRSI"] = str(result_k) + ":" + str(result_d)

    if result_k < 20 and result_d < 20:
        result["SRSI"] = result["SRSI"] + "-up:"
        underpriced = underpriced + 1
        # under priced

    elif result_k > 80 and result_d > 80:
        result["SRSI"] = result["SRSI"] + "-op:"
        overpriced = overpriced + 1
        # over priced

    else:
        result["SRSI"] = result["SRSI"] + "-ne:"
        # neutral

    if result_k >= result_d:
        result["SRSI"] = result["SRSI"] + "bull"
        bull = bull + 1
        # bullish
    else:
        result["SRSI"] = result["SRSI"] + "bear"
        bear = bear + 1
        # bearish

    # BollingerBands - may need a little more work
    result["BB"] = ""

    if abs(result_bbh - result_close) < (proximity_factor):
        result["BB"] = result["BB"] + "op:"
        overpriced = overpriced + 1
        # overpriced

    elif abs(result_close - result_bbl) < (proximity_factor):
        result["BB"] = result["BB"] + "up:"
        underpriced = underpriced + 1
        # underpriced

    else:
        result["BB"] = result["BB"] + "ne:"
        # neutral

    if result_bbh > result_close and result_close > result_bbm:
        result["BB"] = result["BB"] + "bull"
        bull = bull + 1
        # bullish

    elif result_close > result_bbl and result_bbm > result_close:
        result["BB"] = result["BB"] + "bear"
        bear = bear + 1
        # bearish

    # MACD - may need a little more finesse
    result["MACD"] = str(result_macd) + ":" + str(result_macd_s)

    if result_macd > 2 and result_macd_s > 2:
        result["MACD"] = result["MACD"] + "-op:"
        overpriced = overpriced + 1
        # overpriced

    elif result_macd < -2 and result_macd_s < -2:
        result["MACD"] = result["MACD"] + "-up:"
        underpriced = underpriced + 1
        # underpriced

    else:
        result["MACD"] = result["MACD"] + "-ne:"
        # neutral

    if result_macd >= result_macd_s:
        result["MACD"] = result["MACD"] + "bull"
        bull = bull + 1
        # bullish
    else:
        result["MACD"] = result["MACD"] + "bear"
        bear = bear + 1
        # bearish

    # VWAP
    result["VWAP"] = str(result_vwap)

    if result_vwap >= result_close:
        result["VWAP"] = result["VWAP"] + "-bull:"
        bull = bull + 1
        if abs(result_vwap - result_close) < (proximity_factor * 1.2):
            result["VWAP"] = result["VWAP"] + "op"
        else:
            result["VWAP"] = result["VWAP"] + "ne"

    else:
        result["VWAP"] = result["VWAP"] + "-bear:"
        bear = bear + 1
        if abs(result_vwap - result_close) < (proximity_factor * 1.2):
            result["VWAP"] = result["VWAP"] + "up"
        else:
            result["VWAP"] = result["VWAP"] + "ne"

    result["PR"] = str(underpriced) + "/" + str(overpriced)
    result["BU"] = str(bull) + "/" + str(bear)

    return result


def nvt_analysis(exchange, gcei_resp):  # blood, sweat, tears
    client = CoinMetricsClient()
    data = get_current_exchange_info(exchange, gcei_resp)
    base_asset = [get_current_exchange_info(exchange, gcei_resp)['b'].lower()]

    tt = time.localtime(int(time.time()) - 89400 * 720)  # two years ago
    start_time = time.strftime("%Y%m%d", tt)

    try:
        df_metrics = client.get_asset_metrics(
            assets=base_asset, metrics=["NVTAdj90"],
            start_time=start_time).to_dataframe()["NVTAdj90"]
    except Exception as e:
        print("\nno nvt data for this coin")
        return (-999)

    # calculating how many standard_dev away
    # from the historical average
    # todays nvt signal is
    # result is an oscillating indicator
    # derived of nvt, totally analysable
    standard_dev = df_metrics.std()
    h_avg = df_metrics.sum() / len(df_metrics)
    result = (df_metrics[len(df_metrics) - 1] - h_avg) / standard_dev

    print(result)
    print(type(result))
    return (float("{0:.3f}".format(result)))
