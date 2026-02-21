import telebot, requests, os, time
from flask import Flask
from threading import Thread

bot = telebot.TeleBot(os.environ.get("TELEGRAM_TOKEN"))
app = Flask(__name__)

@bot.message_handler(func=lambda m: True)
def chat(m):
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={os.environ.get('GEMINI_KEY')}"
    try:
        data = {"contents": [{"parts": [{"text": "Ты Директор: " + m.text}]}]}
        r = requests.post(url, json=data, timeout=30)
        bot.reply_to(m, r.json()['candidates'][0]['content']['parts'][0]['text'])
    except:
        bot.reply_to(m, "Система онлайн.")

@app.route('/')
def home(): return "Empire Online"

def run_web():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

Thread(target=run_web, daemon=True).start()
bot.remove_webhook()
bot.infinity_polling()
