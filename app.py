import telebot
import os
import google.generativeai as genai
from flask import Flask
from threading import Thread

# 1. Считываем ключи (проверь, что в Render Environment они вписаны!)
TOKEN = os.environ.get("TELEGRAM_TOKEN")
G_KEY = os.environ.get("GEMINI_KEY")

# Инициализация ИИ
genai.configure(api_key=G_KEY)
model = genai.GenerativeModel('gemini-1.5-pro')

# Инициализация Бота
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def health():
    return "EMPIRE ONLINE", 200

# Главный обработчик
@bot.message_handler(func=lambda m: True)
def answer(m):
    print(f"--- НОВОЕ СООБЩЕНИЕ: {m.text} ---")
    try:
        response = model.generate_content(f"Ты Директор Системы. Ответь: {m.text}")
        bot.reply_to(m, response.text)
    except Exception as e:
        print(f"ОШИБКА ГЕМИНИ: {e}")
        bot.reply_to(m, "Ошибка связи с ядром ИИ.")

if __name__ == "__main__":
    # Запускаем Flask на фоне, чтобы Render видел живой порт
    server = Thread(target=lambda: app.run(host="0.0.0.0", port=10000))
    server.daemon = True
    server.start()
    
    print("--- БОТ ВЫХОДИТ НА СВЯЗЬ ---")
    # Запускаем бота основным процессом
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
