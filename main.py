import telebot
import requests
import os
from flask import Flask
from threading import Thread

# Берем ключи из секретного хранилища Render (Environment Variables)
TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_KEY = os.environ.get("GEMINI_KEY")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "Empire System Online. Director is active."

def run_web():
    # Render сам подставит нужный порт
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

@bot.message_handler(func=lambda m: True)
def chat(m):
    # Если ключи не подтянулись, бот скажет об этом
    if not GEMINI_KEY:
        bot.reply_to(m, "Ошибка: Ключ API не найден в настройках сервера.")
        return

    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
    headers = {'Content-Type': 'application/json'}
    data = {"contents": [{"parts": [{"text": "Ты Директор системы Империя. Отвечай кратко и по делу. Вопрос: " + m.text}]}]}
    
    try:
        r = requests.post(url, json=data, headers=headers, timeout=30)
        response_json = r.json()
        
        if 'candidates' in response_json:
            text = response_json['candidates'][0]['content']['parts'][0]['text']
            bot.reply_to(m, text)
        else:
            bot.reply_to(m, f"Ошибка ИИ: {response_json.get('error', {}).get('message', 'Неизвестный сбой')}")
    except Exception as e:
        bot.reply_to(m, "Система: Обрыв связи с ядром.")

if name == "__main__":
    # Запуск веб-сервера для Render в отдельном потоке
    Thread(target=run_web).start()
    
    print("--- ИМПЕРИЯ: ДИРЕКТОР ЗАПУЩЕН ---")
    bot.remove_webhook()
    bot.infinity_polling()
