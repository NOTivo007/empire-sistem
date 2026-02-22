import telebot
import os
import google.generativeai as genai
from flask import Flask, request

# Данные из Environment
TOKEN = os.environ.get("TELEGRAM_TOKEN")
G_KEY = os.environ.get("GEMINI_KEY")
RENDER_URL = f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}"

# Настройка ИИ
genai.configure(api_key=G_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@app.route('/')
def webhook():
    bot.remove_webhook()
    # Установка нового вебхука на твой URL Render
    bot.set_webhook(url=RENDER_URL + '/' + TOKEN)
    return "WEBHOOK SET", 200

@bot.message_handler(func=lambda m: True)
def answer(m):
    print(f"ПОЛУЧЕНО: {m.text}")
    try:
        response = model.generate_content(f"Ты Директор Системы. Ответь: {m.text}")
        bot.reply_to(m, response.text)
    except Exception as e:
        bot.reply_to(m, f"Ошибка ИИ: {str(e)[:50]}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
