import telebot
import os
import google.generativeai as genai
from flask import Flask
from threading import Thread

# Настройка ключей
TOKEN = os.environ.get("TELEGRAM_TOKEN")
G_KEY = os.environ.get("GEMINI_KEY")

# Инициализация Google AI
genai.configure(api_key=G_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@bot.message_handler(func=lambda m: True)
def answer(m):
    try:
        # Официальный метод генерации
        response = model.generate_content(m.text)
        bot.reply_to(m, response.text)
    except Exception as e:
        # Выводим реальную причину, чтобы понять, в VPN ли дело
        bot.reply_to(m, f"Ошибка доступа: {str(e)}")

@app.route('/')
def home(): return "Empire System Live"

def run():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

# Старт
Thread(target=run, daemon=True).start()
bot.remove_webhook()
bot.infinity_polling()
