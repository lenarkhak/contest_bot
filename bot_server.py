notepad bot_server.py
cd contest_bot
nano bot_server.py
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
    url = f"{API_URL}/setWebhook"
    resp = requests.post(url, data={"url": WEBHOOK_URL})
    print("Webhook set:", resp.json())

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
