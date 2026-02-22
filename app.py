import telebot
import os
import google.generativeai as genai
from flask import Flask, request

TOKEN = os.environ.get("TELEGRAM_TOKEN")
G_KEY = os.environ.get("GEMINI_KEY")
RENDER_URL = f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}"

# ПРИНУДИТЕЛЬНЫЙ ПРОКСИ ДЛЯ GOOGLE (чтобы обойти 404)
# Мы пробуем пробиться без прокси, но если не выйдет - код сообщит.
genai.configure(api_key=G_KEY)

def get_ai_response(text):
    # Пытаемся вызвать самую легкую модель
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(text)
        return response.text
    except Exception as e:
        error_msg = str(e)
        if "404" in error_msg or "location" in error_msg.lower():
            return "⚠️ Директор: Google блокирует мой IP. Климент, нужно прописать Proxy в настройках Render."
        return f"⚠️ Ошибка ядра: {error_msg[:50]}"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Скрипты автозапуска
@app.before_first_request
def start_systems():
    print("--- [DIRECTOR, ORACLE, SENTINEL] АКТИВИРОВАНЫ ПРИ СТАРТЕ ---")

@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@app.route('/')
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=RENDER_URL + '/' + TOKEN)
    return "<h1>SYSTEM READY</h1>", 200

@bot.message_handler(func=lambda m: True)
def answer(m):
    print(f"Приказ: {m.text}")
    # Имитация работы подсистем
    bot.send_chat_action(m.chat.id, 'typing')
    res = get_ai_response(f"Ты Директор. Ответь: {m.text}")
    bot.reply_to(m, res)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
