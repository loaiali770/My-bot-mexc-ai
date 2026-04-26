import ccxt
import pandas as pd
import time

exchange = ccxt.mexc({"enableRateLimit": True})

_cache = []
_last = 0

def get_symbols():
    global _cache, _last

    if time.time() - _last < 300:
        return _cache

    tickers = exchange.fetch_tickers()
    symbols = []

    for s, t in tickers.items():
        if "/USDT" in s and t.get("last") and t["last"] <= 0.001:
            if t.get("quoteVolume", 0) > 10000:
                symbols.append(s)

    _cache = symbols[:20]
    _last = time.time()
    return _cache

def get_ohlcv(symbol):
    bars = exchange.fetch_ohlcv(symbol, timeframe="1m", limit=50)
    return pd.DataFrame(bars, columns=['ts','o','h','l','c','v'])
