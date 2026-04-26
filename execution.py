from storage import *
from ai_model import load_model, predict
from features import extract_features

model = load_model()

def handle_trade(symbol, price, score, df):
    balance = get_balance()
    positions = get_positions()

    features = extract_features(df)

    if predict(model, features) == 0:
        return

    if symbol not in positions and score >= 75:
        amount = balance * 0.1
        update_balance(balance - amount)
        save_position(symbol, price, amount)
        print("BUY", symbol)
