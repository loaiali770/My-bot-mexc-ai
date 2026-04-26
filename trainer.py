import sqlite3
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
import joblib

def train():
    conn = sqlite3.connect("bot.db")
    df = pd.read_sql("SELECT * FROM trades", conn)

    if len(df) < 50:
        return

    df['target'] = (df['pnl'] > 0).astype(int)

    X = df[['entry','exit']]
    y = df['target']

    model = GradientBoostingClassifier()
    model.fit(X, y)

    joblib.dump(model, "model.pkl")
