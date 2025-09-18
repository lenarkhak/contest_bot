# bot_server.py
# Telegram бот через Flask + Webhook для Railway

import os
import requests
from flask import Flask, request

app = Flask(__name__)

# Загружаем токен и URL из переменных окружения (.env)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

# ============================
# Установка webhook (один раз)
# ============================
def set_webhook():
    try:
        url = f"{API_URL}/setWebhook"
        webhook_url = f"{WEBHOOK_URL}/webhook"
        
        # Устанавливаем webhook с более подробными параметрами
        data = {
            "url": webhook_url,
            "max_connections": 100,
            "allowed_updates": ["message", "callback_query"]
        }
        
        resp = requests.post(url, json=data, timeout=10)
        result = resp.json()
        print("Webhook set:", result)
        
        if not result.get("ok"):
            print("Error details:", result.get("description"))
            
        return result
    except Exception as e:
        print("Error setting webhook:", str(e))
        return {"ok": False, "error": str(e)}

# ============================
# Обработка входящих сообщений
# ============================
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
    url = f"{API_URL}/sendMessage"
    requests.post(url, data={"chat_id": chat_id, "text": text})


# ============================
# Запуск
# ============================
if __name__ == "__main__":
    # Устанавливаем webhook при запуске
    set_webhook()

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)




