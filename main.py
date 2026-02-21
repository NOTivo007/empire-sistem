
import telebot
import requests
from flask import Flask
from threading import Thread
import os

TOKEN = "8574685716:AAHxX29FDxENc2bq55p8UyS3j3f-lvFTWRw"
GEMINI_KEY = "AIzaSyBeJQF_wWB3OorqqW6hJWzufey12RBaTLQ"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "Empire System Online"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

@bot.message_handler(func=lambda m: True)
def chat(m):
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
    headers = {'Content-Type': 'application/json'}
    data = {"contents": [{"parts": [{"text": "Ты Директор системы Империя. Отвечай кратко: " + m.text}]}]}
    try:
        r = requests.post(url, json=data, headers=headers, timeout=30)
        bot.reply_to(m, r.json()['candidates'][0]['content']['parts'][0]['text'])
    except:
        bot.reply_to(m, "Ошибка связи.")

if name == "__main__":
    Thread(target=run_web).start()
    bot.remove_webhook()
    bot.infinity_polling()
