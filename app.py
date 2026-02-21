import telebot
import requests
import os
from flask import Flask
from threading import Thread
import time

# 1. Получаем ключи из секретов Render
TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_KEY = os.environ.get("GEMINI_KEY")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# --- МОДУЛИ СИСТЕМЫ ---

def oracle_process():
    print("--- ORACLE ONLINE ---")
    while True:
        time.sleep(3600)

def sentinel_process():
    print("--- SENTINEL ONLINE ---")
    while True:
        time.sleep(3600)

# --- ЛОГИКА ДИРЕКТОРА (ИИ) ---

@bot.message_handler(func=lambda m: True)
def chat(m):
    if not GEMINI_KEY:
        bot.reply_to(m, "Ошибка: Ключ GEMINI_KEY не задан.")
        return
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
    headers = {'Content-Type': 'application/json'}
    data = {"contents": [{"parts": [{"text": "Ты Директор системы Империя. Отвечай кратко: " + m.text}]}]}
    try:
        r = requests.post(url, json=data, headers=headers, timeout=30)
        bot.reply_to(m, r.json()['candidates'][0]['content']['parts'][0]['text'])
    except:
        bot.reply_to(m, "Сбой связи.")

# --- ВЕБ-ИНТЕРФЕЙС ---

@app.route('/')
def home():
    return "Empire Active"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# --- ЗАПУСК ---

if name == "__main__":
    Thread(target=run_web, daemon=True).start()
    Thread(target=oracle_process, daemon=True).start()
    Thread(target=sentinel_process, daemon=True).start()
    bot.remove_webhook()
    bot.infinity_polling()
