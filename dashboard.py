import streamlit as st
from storage import get_balance, get_positions
from control import load_state, save_state

st.set_page_config(layout="wide")

st.title("🤖 Trading Bot Control Panel")

state = load_state()
balance = get_balance()
positions = get_positions()

# معلومات عامة
col1, col2, col3 = st.columns(3)

col1.metric("💰 Balance", f"{balance:.2f} USDT")
col2.metric("📊 Open Trades", len(positions))
col3.metric("⚙️ Status", "Running" if state["running"] else "Stopped")

st.divider()

# التحكم
col1, col2 = st.columns(2)

if col1.button("▶️ Start Bot"):
    state["running"] = True
    save_state(state)

if col2.button("⏹ Stop Bot"):
    state["running"] = False
    save_state(state)

# إضافة رصيد
st.subheader("💵 Add Balance")

amount = st.number_input("Enter amount", min_value=0.0)

if st.button("Add Funds"):
    from storage import update_balance
    update_balance(balance + amount)
    st.success("Balance updated")

# عرض الصفقات
st.subheader("📂 Open Positions")

for sym, pos in positions.items():
    st.write(f"""
    🔹 {sym}  
    Entry: {pos['entry']}  
    Max Price: {pos['max']}  
    Amount: {pos['amount']}  
    """)

st.autorefresh(interval=5000)
