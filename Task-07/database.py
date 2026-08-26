import sqlite3

DB_NAME = 'berry_broker.db'

def get_connection():
    return sqlite3.connect(DB_NAME)

def setup():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            balance INTEGER DEFAULT 100,
            last_daily REAL DEFAULT 0,
            last_rob REAL DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

def get_user(user_id, username):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = c.fetchone()
    
    if not user:
        c.execute('INSERT INTO users (user_id, username, balance, last_daily, last_rob) VALUES (?, ?, ?, ?, ?)', 
                  (user_id, username, 100, 0, 0))
        conn.commit()
        user = (user_id, username, 100, 0, 0)
    else:
        if user[1] != username:
            c.execute('UPDATE users SET username = ? WHERE user_id = ?', (username, user_id))
            conn.commit()
            
    conn.close()
    return user

def update_balance(user_id, amount):
    conn = get_connection()
    c = conn.cursor()
    c.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (amount, user_id))
    conn.commit()
    conn.close()

def update_cooldown(user_id, col, timestamp):
    conn = get_connection()
    c = conn.cursor()
    c.execute(f'UPDATE users SET {col} = ? WHERE user_id = ?', (timestamp, user_id))
    conn.commit()
    conn.close()

def get_top_users(limit=5):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT username, balance FROM users ORDER BY balance DESC LIMIT ?', (limit,))
    users = c.fetchall()
    conn.close()
    return users