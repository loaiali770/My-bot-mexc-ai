import numpy as np

def safe_div(a, b):
    if b is None or b == 0 or np.isnan(b):
        return 0
    return a / b

def extract_features(df):
    try:
        if len(df) < 20:
            return [0, 0, 0, 0, 0]

        last = df.iloc[-1]
        prev = df.iloc[-2]

        ema_diff = last['ema8'] - last['ema21']

        price_change = safe_div(
            (last['c'] - prev['c']),
            prev['c']
        )

        vol_mean = df['v'].rolling(10).mean().iloc[-1]
        volume_ratio = safe_div(last['v'], vol_mean)

        volatility = (df['h'] - df['l']).rolling(10).mean().iloc[-1]
        if np.isnan(volatility):
            volatility = 0

        rsi = last['rsi']
        if np.isnan(rsi):
            rsi = 50

        return [
            ema_diff,
            price_change,
            volume_ratio,
            volatility,
            rsi
        ]

    except Exception as e:
        print("Feature Error:", e)
        return [0, 0, 0, 0, 0]
