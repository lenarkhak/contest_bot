# bot_server.py
# Telegram бот через Flask + Webhook для Railway

import os
import requests
from flask import Flask, request

app = Flask(__name__)

# Загружаем токен и URL из переменных окружения
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

# ============================
# Установка webhook
# ============================
@app.route("/webhook", methods=["POST"])
def webhook():
    update = request.get_json()
    
    # Детальное логирование для отладки
    print("=== INCOMING REQUEST ===")
    print(f"Update: {update}")
    
    if not update:
        print("Empty update received")
        return "ok"

    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        user_id = update["message"]["from"]["id"]  # Это ваш Telegram ID
        text = update["message"].get("text", "")
        
        # Логируем информацию о пользователе
        print(f"User ID: {user_id}")
        print(f"Chat ID: {chat_id}")
        print(f"Message text: {text}")
        
        # Отвечаем пользователю с его ID
        reply_text = f"Ваш Telegram ID: {user_id}\nChat ID: {chat_id}\nВы написали: {text}"
        send_message(chat_id, reply_text)

    return "ok"
# ============================
# Обработка входящих сообщений
# ============================
@app.route("/")
def index():
    return "Bot is running!"

@app.route("/set_webhook")
def set_webhook_route():
    """Ручная установка webhook через браузер"""
    result = set_webhook()
    return result

@app.route("/delete_webhook")
def delete_webhook_route():
    """Удаление webhook через браузер"""
    try:
        url = f"{API_URL}/deleteWebhook"
        resp = requests.post(url, timeout=10)
        result = resp.json()
        return result
    except Exception as e:
        return {"ok": False, "error": str(e)}

@app.route("/webhook", methods=["POST"])
def webhook():
    update = request.get_json()

    if not update:
        return "ok"

    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"].get("text", "")

        # Ответ пользователю
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








