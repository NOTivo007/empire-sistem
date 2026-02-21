import telebot, requests, os, time
from flask import Flask
from threading import Thread

TOKEN = os.environ.get("TELEGRAM_TOKEN")
G_KEY = os.environ.get("GEMINI_KEY")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@bot.message_handler(func=lambda m: True)
def answer(m):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={G_KEY}"
    payload = {"contents": [{"parts": [{"text": m.text}]}]}
    try:
        response = requests.post(url, json=payload, timeout=20)
        data = response.json()
        if "candidates" in data:
            reply = data["candidates"][0]["content"]["parts"][0]["text"]
            bot.reply_to(m, reply)
        else:
            bot.reply_to(m, f"Google Error: {data.get('error', {}).get('message', 'No text')}")
    except Exception as e:
        bot.reply_to(m, f"Core Crash: {str(e)}")

@app.route('/')
def home(): return "Empire Online"

def run():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

# ПРЯМОЙ ЗАПУСК БЕЗ ПРОВЕРОК
print("--- BOOTING SYSTEM ---")
Thread(target=run, daemon=True).start()
bot.remove_webhook()
bot.infinity_polling()
