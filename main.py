import time
from data import get_symbols, get_ohlcv
from strategy import calculate_indicators, get_signal
from execution import handle_trade
import trainer

while True:
    symbols = get_symbols()

    for s in symbols:
        df = get_ohlcv(s)
        df = calculate_indicators(df)

        score = get_signal(df)
        price = df.iloc[-1]['c']

        handle_trade(s, price, score, df)

    if int(time.time()) % 3600 < 10:
        trainer.train()

    time.sleep(10)
