import sqlite3
import datetime
import os

# Функция инициализации базы данных
def init_db():
    # Подключаемся к базе данных (файл bot.db будет создан автоматически)
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    
    # Создаем таблицу пользователей, если она не существует
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  chat_id INTEGER UNIQUE,
                  username TEXT,
                  first_name TEXT,
                  last_name TEXT,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    # Создаем таблицу сообщений, если она не существует
    c.execute('''CREATE TABLE IF NOT EXISTS messages
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  chat_id INTEGER,
                  message_text TEXT,
                  message_date TIMESTAMP,
                  is_deleted BOOLEAN DEFAULT FALSE,
                  FOREIGN KEY (chat_id) REFERENCES users (chat_id))''')
    
    # Создаем таблицу забаненных пользователей, если она не существует
    c.execute('''CREATE TABLE IF NOT EXISTS banned_users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  chat_id INTEGER UNIQUE,
                  banned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  reason TEXT,
                  FOREIGN KEY (chat_id) REFERENCES users (chat_id))''')
    
    # Создаем таблицу логов административных действий, если она не существует
    c.execute('''CREATE TABLE IF NOT EXISTS admin_logs
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  admin_id INTEGER,
                  action TEXT,
                  target_id INTEGER,
                  details TEXT,
                  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    # Сохраняем изменения и закрываем соединение
    conn.commit()
    conn.close()

# Вызываем инициализацию базы данных при запуске приложения
init_db()       
# bot_server.py
# Telegram бот через Flask + Webhook для Railway

import os
import requests
from flask import Flask, request

app = Flask(__name__)

# Загружаем токен и URL из переменных окружения
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
ADMIN_ID = os.getenv("ADMIN_ID")  # Добавляем загрузку ADMIN_ID
API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

# ============================
# Установка webhook
# ============================
def set_webhook():
    try:
        url = f"{API_URL}/setWebhook"
        webhook_url = f"{WEBHOOK_URL}/webhook"
        
        data = {
            "url": webhook_url,
            "max_connections": 100,
            "allowed_updates": ["message"]
        }
        
        resp = requests.post(url, json=data, timeout=10)
        result = resp.json()
        print("Webhook set:", result)
        
        return result
    except Exception as e:
        print("Error setting webhook:", str(e))
        return {"ok": False, "error": str(e)}

# ============================
# Обработка входящих сообщений
# ============================
@app.route("/")
def index():
    return "Bot is running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    update = request.get_json()

    if not update:
        return "ok"

    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"].get("text", "")

        # Ответ пользователю (исходная версия)
        reply_text = f"Ты написал: {text}"
        send_message(chat_id, reply_text)

    return "ok"

def send_message(chat_id, text):
    try:
        url = f"{API_URL}/sendMessage"
        data = {
            "chat_id": chat_id,
            "text": text
        }
        requests.post(url, json=data, timeout=5)
    except Exception as e:
        print("Error sending message:", str(e))

# ============================
# Запуск приложения
# ============================
if __name__ == "__main__":
    # Устанавливаем webhook при запуске
    set_webhook()

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)










