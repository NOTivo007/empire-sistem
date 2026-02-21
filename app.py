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

def oracle_process():
    while True: time.sleep(3600)

def sentinel_process():
    while True: time.sleep(3600)

@bot.message_handler(func=lambda m: True)
def chat(m):
    if not GEMINI_KEY:
        bot.reply_to(m, "Ошибка: Ключ GEMINI_KEY не найден в Environment Variables!")
        return
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
    headers = {'Content-Type': 'application/json'}
    data = {"contents": [{"parts": [{"text": "Ты Директор системы Империя: " + m.text}]}]}
    
    try:
        r = requests.post(url, json=data, headers=headers, timeout=30)
        res = r.json()
        
        # Если в ответе есть текст - выводим
        if 'candidates' in res:
            text = res['candidates'][0]['content']['parts'][0]['text']
            bot.reply_to(m, text)
        else:
            # Если Google прислал ошибку - пишем какую
            error_msg = res.get('error', {}).get('message', 'Неизвестная ошибка API')
            bot.reply_to(m, f"Ошибка от Google: {error_msg}")
    except Exception as e:
        bot.reply_to(m, f"Ошибка связи: {str(e)}")

@app.route('/')
def home(): return "Empire Online"

def run_web():
    p = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=p)

Thread(target=run_web, daemon=True).start()
Thread(target=oracle_process, daemon=True).start()
Thread(target=sentinel_process, daemon=True).start()

bot.remove_webhook()
bot.infinity_polling()
