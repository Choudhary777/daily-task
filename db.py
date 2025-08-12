import sqlite3

def create_table():
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_data (
            username TEXT PRIMARY KEY,
            pendingtask TEXT NOT NULL,
            completedtask TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
def insert_user_data(username, pendingtask, completedtask):
    # print("pendingtask", pendingtask, "completedtask", completedtask)
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    cursor.execute("REPLACE INTO user_data (username, pendingtask, completedtask) VALUES (?, ?, ?)", (username, pendingtask, completedtask))
    conn.commit()
    conn.close()
    # print("Data inserted successfully")
def get_user_data(username):
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    cursor.execute("SELECT pendingtask, completedtask FROM user_data WHERE username=?", (username,))
    user_data = cursor.fetchone()
    # print("user_data", user_data)
    conn.close()
    return user_data
def check_username(username):
    username_ = username.lower()
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=?", (username_,))
    user = cursor.fetchone()
    conn.close()
    return user
def check_user(username, password):
    username_ = username.lower()
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username_, password))
    user = cursor.fetchone()
    conn.close()
    return user
def insert_user(username, password):
    username_ = username.lower()
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username_, password))
    conn.commit()
    conn.close()
def drop_table():
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS user_data")
    conn.commit()
    conn.close()