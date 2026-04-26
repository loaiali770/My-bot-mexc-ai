import numpy as np

def safe_div(a, b):
    try:
        if b == 0 or b is None or np.isnan(b):
            return 0
        return a / b
    except:
        return 0


def extract_features(df):
    try:
        # تأكد من وجود بيانات كافية
        if df is None or len(df) < 20:
            return [0, 0, 0, 0, 0]

        last = df.iloc[-1]
        prev = df.iloc[-2]

        # EMA
        ema8 = last.get('ema8', 0)
        ema21 = last.get('ema21', 0)
        ema_diff = ema8 - ema21

        # Price change
        prev_close = prev.get('c', 1)
        last_close = last.get('c', 1)
        price_change = safe_div((last_close - prev_close), prev_close)

        # Volume ratio
        vol_mean = df['v'].rolling(10).mean().iloc[-1]
        volume_ratio = safe_div(last.get('v', 0), vol_mean)

        # Volatility
        volat = (df['h'] - df['l']).rolling(10).mean().iloc[-1]
        if volat is None or np.isnan(volat):
            volat = 0

        # RSI
        rsi = last.get('rsi', 50)
        if rsi is None or np.isnan(rsi):
            rsi = 50

        return [
            float(ema_diff),
            float(price_change),
            float(volume_ratio),
            float(volat),
            float(rsi)
        ]

    except Exception as e:
        print("Feature Error:", e)
        return [0, 0, 0, 0, 0]
