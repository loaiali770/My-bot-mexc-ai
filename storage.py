import sqlite3

conn = sqlite3.connect("bot.db", check_same_thread=False)
c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS balance (id INTEGER PRIMARY KEY, value REAL)")
c.execute("CREATE TABLE IF NOT EXISTS positions (symbol TEXT, entry REAL, max REAL, amount REAL)")
c.execute("CREATE TABLE IF NOT EXISTS trades (symbol TEXT, entry REAL, exit REAL, pnl REAL, time TEXT)")

conn.commit()

def get_balance():
    row = c.execute("SELECT value FROM balance WHERE id=1").fetchone()
    if row:
        return row[0]
    c.execute("INSERT INTO balance VALUES (1, 100)")
    conn.commit()
    return 100

def update_balance(v):
    c.execute("UPDATE balance SET value=? WHERE id=1", (v,))
    conn.commit()

def get_positions():
    rows = c.execute("SELECT * FROM positions").fetchall()
    return {r[0]: {"entry": r[1], "max": r[2], "amount": r[3]} for r in rows}

def save_position(s, e, a):
    c.execute("INSERT INTO positions VALUES (?, ?, ?, ?)", (s, e, e, a))
    conn.commit()

def update_max(s, p):
    c.execute("UPDATE positions SET max=? WHERE symbol=?", (p, s))
    conn.commit()

def remove_position(s):
    c.execute("DELETE FROM positions WHERE symbol=?", (s,))
    conn.commit()
