def calculate_indicators(df):
    df['ema8'] = df['c'].ewm(span=8).mean()
    df['ema21'] = df['c'].ewm(span=21).mean()

    df['rsi'] = 100 - (100 / (1 + df['c'].pct_change().rolling(14).mean()))
    return df

def get_signal(df):
    last = df.iloc[-1]
    prev = df.iloc[-2]

    score = 0

    if last['ema8'] > last['ema21'] and prev['ema8'] <= prev['ema21']:
        score += 30

    if 25 < last['rsi'] < 40:
        score += 20

    if last['c'] > prev['c']:
        score += 20

    if last['v'] > df['v'].rolling(10).mean().iloc[-1]:
        score += 15

    if df['ema21'].iloc[-1] > df['ema21'].iloc[-5]:
        score += 15

    return score
