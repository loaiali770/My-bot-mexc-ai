from storage import (
    get_balance,
    update_balance,
    get_positions,
    save_position,
    update_max,
    remove_position
)

from features import extract_features
from ai_model import load_model, predict

import config
import math

# تحميل النموذج مرة واحدة
model = load_model()


def is_invalid(features):
    """
    التحقق من وجود قيم غير صالحة
    """
    if features is None:
        return True

    for f in features:
        if f is None:
            return True
        if isinstance(f, float) and (math.isnan(f) or math.isinf(f)):
            return True

    return False


def handle_trade(symbol, price, score, df):
    balance = get_balance()
    positions = get_positions()

    # 🧠 استخراج الخصائص
    features = extract_features(df)

    # 🛑 حماية من البيانات الفاسدة
    if is_invalid(features):
        return

    # 🧠 قرار الذكاء الاصطناعي
    ai_decision = predict(model, features)

    if ai_decision == 0:
        return

    # =========================
    # 🔴 إدارة الصفقات المفتوحة (SELL)
    # =========================
    if symbol in positions:
        pos = positions[symbol]

        entry = pos["entry"]
        max_price = pos["max"]
        amount = pos["amount"]

        # تحديث أعلى سعر
        if price > max_price:
            update_max(symbol, price)
            return

        # حساب التراجع (Trailing Stop)
        drop = (max_price - price) / max_price

        if drop >= config.TRAILING_STOP:
            profit = (price - entry) / entry
            pnl = amount * profit

            balance += amount + pnl
            update_balance(balance)

            remove_position(symbol)

            print(f"SELL {symbol} | PnL: {pnl:.4f}")

        return

    # =========================
    # 🟢 دخول صفقة (BUY)
    # =========================
    else:
        # حد أقصى للصفقات
        if len(positions) >= config.MAX_OPEN_TRADES:
            return

        # شرط الاستراتيجية الأصلية
        if score >= 75 and balance > 1:
            amount = balance * config.RISK_PER_TRADE

            balance -= amount
            update_balance(balance)

            save_position(symbol, price, amount)

            print(f"BUY {symbol} | Amount: {amount:.2f}")
