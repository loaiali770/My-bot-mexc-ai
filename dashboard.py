import streamlit as st
from storage import get_balance

st.title("Trading Bot")

st.metric("Balance", get_balance())

st.write("Bot running in background...")
