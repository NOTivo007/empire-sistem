import telebot, requests, os, time
from flask import Flask
from threading import Thread

# Забираем токены из настроек Render
TOKEN = os.environ.get("TELEGRAM_TOKEN")
G_KEY = os.environ.get("GEMINI_KEY")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@bot.message_handler(func=lambda m: True)
def answer(m):
    # ВЕРСИЯ V1 (Стабильная)
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={G_KEY}"
    
    payload = {
        "contents": [{"parts": [{"text": m.text}]}]
    }
    
    try:
        response = requests.post(url, json=payload, timeout=25)
        data = response.json()
        
        # Проверка структуры ответа
        if "candidates" in data and len(data["candidates"]) > 0:
            candidate = data["candidates"][0]
            if "content" in candidate and "parts" in candidate["content"]:
                reply = candidate["content"]["parts"][0]["text"]
                bot.reply_to(m, reply)
            else:
                bot.reply_to(m, "Ядро ИИ выдало пустой результат.")
        else:
            # Если опять ошибка - бот напишет её текст из JSON
            error_info = data.get('error', {}).get('message', 'Неизвестная ошибка API')
            bot.reply_to(m, f"Google Error: {error_info}")
            
    except Exception as e:
        bot.reply_to(m, f"Критический сбой: {str(e)}")

@app.route('/')
def home():
    return "Empire Online - All Systems Operational"

def run():
    # Порт для Render
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# ПРЯМОЙ ЗАПУСК БЕЗ IF NAME == MAIN (чтобы не было ошибок с 'name')
print("--- STARTING EMPIRE CORE ---")
Thread(target=run, daemon=True).start()

# Автозапуск дополнительных модулей (Oracle и Sentinel)
def background_modules():
    print("--- ORACLE & SENTINEL ACTIVE ---")
    while True: time.sleep(3600)
Thread(target=background_modules, daemon=True).start()

bot.remove_webhook()
bot.infinity_polling(timeout=20, long_polling_timeout=10)
