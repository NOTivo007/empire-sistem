import telebot
import os
import google.generativeai as genai
from flask import Flask, request
import time

TOKEN = os.environ.get("TELEGRAM_TOKEN")
G_KEY = os.environ.get("GEMINI_KEY")
RENDER_URL = f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}"

# Наш список прокси для "Моста"
PROXY_LIST = [
    'http://167.172.189.157:3128',
    'http://64.225.8.181:3128',
    'http://159.203.87.130:3128',
    'http://138.68.60.8:3128'
]

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

def get_ai_response(text):
    test_proxies = [None] + PROXY_LIST
    for proxy in test_proxies:
        try:
            if proxy:
                os.environ['https_proxy'] = proxy
                os.environ['http_proxy'] = proxy
            else:
                if 'https_proxy' in os.environ: del os.environ['https_proxy']

            genai.configure(api_key=G_KEY)
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(f"Ты Директор Системы. Ответь: {text}")
            return response.text
        except Exception as e:
            print(f"Пропуск узла {proxy}: {str(e)[:40]}")
            continue
    return "⚠️ Все узлы заблокированы. Климент, проверь ключи."

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
    # Активация систем при первом заходе
    print("--- [DIRECTOR] СИСТЕМА УПРАВЛЕНИЯ В СЕТИ ---")
    print("--- [ORACLE] АНАЛИЗАТОР ЗАПУЩЕН ---")
    print("--- [SENTINEL] ПЕРИМЕТР ПОД ОХРАНОЙ ---")
    return "<h1>BRIDGE ACTIVE</h1>", 200

@bot.message_handler(func=lambda m: True)
def answer(m):
    print(f"Приказ: {m.text}")
    bot.send_chat_action(m.chat.id, 'typing')
    res = get_ai_response(m.text)
    bot.reply_to(m, res)

if __name__ == "__main__":
    # Запуск без before_first_request
    app.run(host="0.0.0.0", port=10000)
