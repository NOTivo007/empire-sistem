import telebot
import os
import google.generativeai as genai
from flask import Flask
from threading import Thread
import time

# Настройка ключей из Render
TOKEN = os.environ.get("TELEGRAM_TOKEN")
G_KEY = os.environ.get("GEMINI_KEY")

# Инициализация Gemini
genai.configure(api_key=G_KEY)
# Используем flash, так как она быстрее для тестов
model = genai.GenerativeModel('gemini-1.5-flash')

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@bot.message_handler(func=lambda m: True)
def answer(m):
    try:
        # Прямой вызов через библиотеку Google
        response = model.generate_content(m.text)
        if response.text:
            bot.reply_to(m, response.text)
        else:
            bot.reply_to(m, "ИИ прислал пустой ответ.")
    except Exception as e:
        # Если будет ошибка региона, она отобразится здесь
        bot.reply_to(m, f"Ошибка доступа: {str(e)}")

@app.route('/')
def home():
    return "Empire System: Online"

def run():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# Запуск фоновых процессов
def background_tasks():
    print("--- ORACLE & SENTINEL ONLINE ---")
    while True:
        time.sleep(3600)

if name == "__main__":
    Thread(target=run, daemon=True).start()
    Thread(target=background_tasks, daemon=True).start()
    
    print("--- EMPIRE CORE STARTED ---")
    bot.remove_webhook()
    bot.infinity_polling()
