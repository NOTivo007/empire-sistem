import telebot
import requests
import os
from flask import Flask
from threading import Thread
import time

TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_KEY = os.environ.get("GEMINI_KEY")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# --- ОРАКУЛ И СЕНТИНЕЛЬ ---
def oracle_process():
    while True: time.sleep(3600)

def sentinel_process():
    while True: time.sleep(3600)

# --- ИИ ДИРЕКТОР ---
@bot.message_handler(func=lambda m: True)
def chat(m):
    # Исправленный URL для стабильной работы Gemini
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
    headers = {'Content-Type': 'application/json'}
    data = {"contents": [{"parts": [{"text": "Ты Директор системы Империя: " + m.text}]}]}
    
    try:
        r = requests.post(url, json=data, headers=headers, timeout=30)
        res = r.json()
        if 'candidates' in res:
            text = res['candidates'][0]['content']['parts'][0]['text']
            bot.reply_to(m, text)
        else:
            bot.reply_to(m, f"Ошибка API: {res.get('error', {}).get('message', 'Неизвестно')}")
    except Exception as e:
        bot.reply_to(m, "Сбой связи.")

@app.route('/')
def home(): return "Empire Online"

def run_web():
    p = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=p)

# СТАРТ СИСТЕМЫ
if name == "__main__":
    Thread(target=run_web, daemon=True).start()
    Thread(target=oracle_process, daemon=True).start()
    Thread(target=sentinel_process, daemon=True).start()
    
    print("--- EMPIRE SYSTEM START ---")
    
    # Решение ошибки 409: Сначала удаляем вебхук, потом ждем, потом запускаем
    bot.remove_webhook()
    time.sleep(1) 
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
