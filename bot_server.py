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
    
    # Добавьте логирование для отладки
    print(f"Incoming update: {update}")
    
    if not update:
        return "ok"

    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"].get("text", "")
        
        # Ответ пользователю
        reply_text = f"Ты написал: {text}"
        send_message(chat_id, reply_text)
        
        # Логируем ID для отладки
        print(f"Message from chat_id: {chat_id}")

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









