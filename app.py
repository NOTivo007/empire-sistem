import telebot
import requests
import os
from flask import Flask
from threading import Thread
import time

# 1. Секреты
TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_KEY = os.environ.get("GEMINI_KEY")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# --- СИСТЕМА ---
def oracle_process():
    while True:
        time.sleep(3600)

def sentinel_process():
    while True:
        time.sleep(3600)

# --- ИИ ---
@bot.message_handler(func=lambda m: True)
def chat(m):
    if not GEMINI_KEY:
        bot.reply_to(m, "No Key")
        return
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
    try:
        data = {"contents": [{"parts": [{"text": "Ты Директор системы Империя: " + m.text}]}]}
        r = requests.post(url, json=data, timeout=30)
        bot.reply_to(m, r.json()['candidates'][0]['content']['parts'][0]['text'])
    except:
        bot.reply_to(m, "Error")

# --- WEB ---
@app.route('/')
def home():
    return "Empire Online"

def run_web():
    p = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=p)

# --- СТАРТ ---
if name == "__main__":
    Thread(target=run_web, daemon=True).start()
    Thread(target=oracle_process, daemon=True).start()
    Thread(target=sentinel_process, daemon=True).start()
    bot.remove_webhook()
    bot.infinity_polling()
