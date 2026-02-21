import telebot, requests, os, time
from flask import Flask
from threading import Thread

TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_KEY = os.environ.get("GEMINI_KEY")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@bot.message_handler(func=lambda m: True)
def chat(m):
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
    try:
        data = {"contents": [{"parts": [{"text": "Ты Директор: " + m.text}]}]}
        r = requests.post(url, json=data, timeout=30)
        bot.reply_to(m, r.json()['candidates'][0]['content']['parts'][0]['text'])
    except:
        bot.reply_to(m, "Система на связи.")

@app.route('/')
def home(): return "Empire Online"

def run_web():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

# Модули Oracle и Sentinel
def system_modules():
    print("--- ORACLE & SENTINEL START ---")
    while True: time.sleep(3600)

Thread(target=run_web, daemon=True).start()
Thread(target=system_modules, daemon=True).start()

print("--- ALL SYSTEMS GO ---")
bot.remove_webhook()
bot.infinity_polling()
