import telebot
import os
import google.generativeai as genai
from flask import Flask
from threading import Thread
import time
import requests

# 1. Загрузка ключей из настроек Render
TOKEN = os.environ.get("TELEGRAM_TOKEN")
G_KEY = os.environ.get("GEMINI_KEY")

# 2. Настройка нейросети
genai.configure(api_key=G_KEY)
# Используем flash-модель, она стабильнее для бесплатных серверов
model = genai.GenerativeModel('gemini-1.5-flash')

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# 3. Веб-сервер для "здоровья" Render
@app.route('/')
def health():
    return "SYSTEM ONLINE", 200

# 4. Логика Директора
@bot.message_handler(func=lambda m: True)
def answer(m):
    print(f"Приказ от Климента: {m.text}")
    try:
        # Формируем личность Директора
        prompt = f"Ты Директор Системы. Твой создатель - Климент. Ответь на приказ: {m.text}"
        response = model.generate_content(prompt)
        bot.reply_to(m, response.text)
    except Exception as e:
        err = str(e)
        print(f"Ошибка: {err}")
        if "location" in err.lower():
            bot.reply_to(m, "⚠️ Ошибка региона! Google не работает в этом дата-центре. Смени регион в настройках Render на Frankfurt.")
        else:
            bot.reply_to(m, f"Ядро ИИ временно недоступно: {err[:50]}...")

# 5. Функция защиты от сна
def keep_alive():
    time.sleep(20) # Ждем запуска сервера
    while True:
        try:
            host = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
            if host:
                requests.get(f"https://{host}.onrender.com/")
                print("Пинг системы выполнен")
        except:
            pass
        time.sleep(600) # Пинг каждые 10 минут

if __name__ == "__main__":
    # Запуск веб-части
    Thread(target=lambda: app.run(host="0.0.0.0", port=10000)).start()
    # Запуск анти-сна
    Thread(target=keep_alive).start()
    # Запуск бота основным потоком
    print("--- ИМПЕРИЯ ВЫШЛА НА СВЯЗЬ ---")
    bot.infinity_polling()
