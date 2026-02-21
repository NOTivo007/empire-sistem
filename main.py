import telebot
import os
import google.generativeai as genai
from flask import Flask
from threading import Thread
import time

# Ключи
TOKEN = os.environ.get("TELEGRAM_TOKEN")
G_KEY = os.environ.get("GEMINI_KEY")

# Инициализация Gemini
genai.configure(api_key=G_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@bot.message_handler(func=lambda m: True)
def answer(m):
    try:
        response = model.generate_content(m.text)
        bot.reply_to(m, response.text if response.text else "Пустой ответ.")
    except Exception as e:
        bot.reply_to(m, f"Ошибка: {str(e)}")

@app.route('/')
def home():
    return "Empire Online"

def run_web():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

# ПРЯМОЙ ЗАПУСК (БЕЗ УСЛОВИЙ)
print("--- SYSTEM START ---")
Thread(target=run_web, daemon=True).start()
bot.remove_webhook()
bot.infinity_polling()
