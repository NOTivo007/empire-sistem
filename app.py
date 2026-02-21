import telebot, requests, os, time
from flask import Flask
from threading import Thread

# Берем ключи
TOKEN = os.environ.get("TELEGRAM_TOKEN")
G_KEY = os.environ.get("GEMINI_KEY")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@bot.message_handler(func=lambda m: True)
def answer(m):
    # Прямой URL к стабильной версии Gemini 1.5 Flash
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={G_KEY}"
    
    payload = {
        "contents": [{"parts": [{"text": m.text}]}]
    }
    
    try:
        response = requests.post(url, json=payload, timeout=20)
        data = response.json()
        
        # Проверка: если в ответе есть текст - шлем его
        if "candidates" in data:
            reply = data["candidates"][0]["content"]["parts"][0]["text"]
            bot.reply_to(m, reply)
        else:
            # Если Google вернул ошибку, бот ПРЯМО напишет её текст
            bot.reply_to(m, f"Ошибка API: {data.get('error', {}).get('message', 'Нет ответа')}")
            
    except Exception as e:
        bot.reply_to(m, f"Сбой в ядре: {str(e)}")

@app.route('/')
def home(): return "Active"

def run():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

if name == "__main__":
    Thread(target=run, daemon=True).start()
    bot.remove_webhook()
    # Ставим большой таймаут, чтобы не было конфликтов 409
    bot.infinity_polling(timeout=20, long_polling_timeout=10)
