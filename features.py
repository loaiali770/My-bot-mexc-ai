def extract_features(df):
    last = df.iloc[-1]
    prev = df.iloc[-2]

    return [
        last['ema8'] - last['ema21'],
        (last['c'] - prev['c']) / prev['c'],
        last['v'] / df['v'].rolling(10).mean().iloc[-1],
        (df['h'] - df['l']).rolling(10).mean().iloc[-1],
        last['rsi']
    ]
