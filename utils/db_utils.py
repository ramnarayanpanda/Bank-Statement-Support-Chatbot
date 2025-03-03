import os
import sqlite3
import hashlib
import json

def setup_database():
    conn = sqlite3.connect("./database/bank_data.db")
    cursor = conn.cursor()

    # Create the table with the specified schema
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            chat_history TEXT
        )
    """)

    conn.commit()
    conn.close()


def register_user(user_id, password):
    conn = sqlite3.connect("./database/bank_data.db")
    cursor = conn.cursor()
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    status = True
    try:
        cursor.execute("""INSERT INTO users (user_id, password, chat_history) VALUES (?, ?, ?)""",
                       (user_id, hashed_password, json.dumps([])))
        conn.commit()
        print(f"User {user_id} registered successfully.")
    except sqlite3.IntegrityError:
        status = False
        print(f"User {user_id} already exists.")
    conn.close()
    return status


def authenticate_user(user_id, password):
    conn = sqlite3.connect("./database/bank_data.db")
    cursor = conn.cursor()
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    cursor.execute("""SELECT id FROM users WHERE user_id = ? AND password = ?""",
                   (user_id, hashed_password))
    result = cursor.fetchone()
    conn.close()
    status = True
    if not result:
        status = False
        print("user_id or password is wrong, please enter correct id or password, or signup as new user")
    return status


def save_conversation_history(user_id, new_message):
    status = True
    conn = sqlite3.connect("./database/bank_data.db")
    cursor = conn.cursor()
    cursor.execute("""SELECT chat_history FROM users WHERE user_id = ?""", (user_id,))
    result = cursor.fetchone()
    if result:
        cursor.execute("""UPDATE users SET chat_history = ? WHERE user_id = ?""",
                       (json.dumps(new_message), user_id))
        conn.commit()
    else:
        status = False
        print(f"No user found with user_id {user_id}.")
    conn.close()
    return status


def load_conversation_history(user_id):
    conn = sqlite3.connect("./database/bank_data.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT chat_history FROM users WHERE user_id = ?
    """, (user_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]
    else:
        return None


def fetch_data():
    conn = sqlite3.connect("./database/bank_data.db")
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM users;""", )
    result = cursor.fetchall()
    return result