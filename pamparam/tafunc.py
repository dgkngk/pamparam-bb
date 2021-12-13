import pandas as pd
import ta


def ta_analyze(candledata):

    result = {}
    close_list = []
    last_h = float(candledata[-1][2])
    last_l = float(candledata[-1][3])

    for trade in candledata:
        close_list.append(float(trade[4]))

    t_c = pd.Series(close_list)
    t_d = ta.momentum.stochrsi_d(
        t_c, window=14, smooth1=3, smooth2=3, fillna=False)
    t_k = ta.momentum.stochrsi_k(
        t_c, window=14, smooth1=3, smooth2=3, fillna=False)

    indicator_bb = ta.volatility.BollingerBands(
        close=t_c, window=20, window_dev=2)

    t_bh = indicator_bb.bollinger_hband()
    t_bl = indicator_bb.bollinger_lband()
    # maybe add strat for squeezes for this
    # half of the standard deviation
    proximity_factor = abs(
        (float(candledata[-1][4]) - t_bh[len(t_bh) - 1]) / 4)

    result["k%"] = float("{0:.3f}".format(t_k[len(t_k) - 1] * 100))
    # some hacking to clear out unnecessary precision
    result["d%"] = float("{0:.3f}".format(t_d[len(t_d) - 1] * 100))
    # result["bh"]=t_bh[len(t_bh)-1]
    # result["bl"]=t_bl[len(t_bl)-1]

    if(t_d[len(t_d) - 1] * 100) < 20 and (t_k[len(t_k) - 1] * 100) < 20:
        if t_d[len(t_d) - 1] < t_k[len(t_k) - 1]:
            if (abs(last_l - t_bl[len(t_bl) - 1]) < proximity_factor):
                result["signal"] = "strong buy"
            else:
                result["signal"] = "weak buy"
        else:
            result["signal"] = "get ready to buy"

    elif(t_d[len(t_d) - 1] * 100) > 80 and (t_k[len(t_k) - 1] * 100) > 80:
        if t_d[len(t_d) - 1] > t_k[len(t_k) - 1]:
            if (abs(last_h - t_bh[len(t_bh) - 1]) < proximity_factor):
                result["signal"] = "strong sell"
            else:
                result["signal"] = "weak sell"
        else:
            result["signal"] = "get ready to sell"

    elif t_d[len(t_d) - 1] < t_k[len(t_k) - 1]:
        result["signal"] = "hold(bull)"
        if (abs(last_l - t_bl[len(t_bl) - 1]) < proximity_factor):
            result["signal"] = "weak buy(bollinger buy)"

    elif t_d[len(t_d) - 1] > t_k[len(t_k) - 1]:
        result["signal"] = "hold(bear)"
        if (abs(last_h - t_bh[len(t_bh) - 1]) < proximity_factor):
            result["signal"] = "weak sell(bollinger sell)"

    else:
        result["k%"] = "not enough"
        result["d%"] = "data gathered"
        result["signal"] = "yet for this coin"

    return result
