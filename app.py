import telebot
import os
import google.generativeai as genai
from flask import Flask
from threading import Thread
import time
import requests

# 1. Настройка ключей
TOKEN = os.environ.get("TELEGRAM_TOKEN")
G_KEY = os.environ.get("GEMINI_KEY")

genai.configure(api_key=G_KEY)
model = genai.GenerativeModel('gemini-1.5-pro')
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

# 2. Логика Директора
@bot.message_handler(func=lambda m: True)
def answer(m):
    try:
        response = model.generate_content(f"Ты Директор Системы. Приказ: {m.text}")
        bot.reply_to(m, response.text)
    except Exception as e:
        print(f"Ошибка Gemini: {e}")

# 3. Веб-интерфейс для Render
@app.route('/')
def health():
    return "EMPIRE CORE IS ACTIVE", 200

def run_flask():
    # Render всегда дает порт 10000
    app.run(host="0.0.0.0", port=10000)

# 4. Система "Анти-сон"
def wake_up():
    # Ждем запуска сервера
    time.sleep(30)
    while True:
        try:
            # Render сам подставляет имя хоста в переменные
            url = f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}.onrender.com/"
            requests.get(url)
            print("Система проснулась сама по себе")
        except:
            print("Пинг не удался, попробуем позже")
        time.sleep(600) # Пинг каждые 10 минут

if __name__ == "__main__":
    # Запускаем Flask в отдельном потоке
    Thread(target=run_flask).start()
    # Запускаем пинг в отдельном потоке
    Thread(target=wake_up).start()
    # Запускаем бота (основной процесс)
    print("--- EMPIRE CORE DEPLOYED ---")
    bot.infinity_polling()
