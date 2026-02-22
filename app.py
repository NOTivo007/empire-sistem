import telebot
import os
import google.generativeai as genai
from flask import Flask, request
import logging

# 1. Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 2. Данные окружения
TOKEN = os.environ.get("TELEGRAM_TOKEN")
G_KEY = os.environ.get("GEMINI_KEY")
# URL твоего приложения на Render (подтягивается автоматически)
RENDER_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
RENDER_URL = f"https://{RENDER_HOSTNAME}"

# 3. Инициализация ИИ (Пробуем версию 1.5-flash)
genai.configure(api_key=G_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# --- АВТОЗАПУСК СИСТЕМ ---
def boot_sequence():
    logger.info(">>> [SYSTEM] Инициализация протоколов...")
    logger.info(">>> [DIRECTOR] Скрипт управления активен.")
    logger.info(">>> [ORACLE] Скрипт прогностики запущен.")
    logger.info(">>> [SENTINEL] Скрипт защиты периметра в сети.")

# --- ОБРАБОТКА WEBHOOK ---
@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return "!", 200
    else:
        return "Error", 403

@app.route('/')
def webhook_setup():
    bot.remove_webhook()
    # Принудительная установка связи с Telegram
    success = bot.set_webhook(url=RENDER_URL + '/' + TOKEN)
    if success:
        return "<h1>SYSTEM ONLINE</h1><p>Director, Oracle, and Sentinel are running in Frankfurt.</p>", 200
    else:
        return "<h1>WEBHOOK ERROR</h1>", 500

# --- КОМАНДЫ И ЛОГИКА ---
@bot.message_handler(commands=['start', 'status'])
def send_status(m):
    status_text = (
        "🤖 **Система Империи: СТАТУС OK**\n"
        "--------------------------\n"
        "✅ **Director:** Мониторинг активен\n"
        "✅ **Oracle:** Поток данных стабилен\n"
        "✅ **Sentinel:** Защита включена\n"
        "--------------------------\n"
        "Климент, я готов к выполнению задач."
    )
    bot.reply_to(m, status_text, parse_mode="Markdown")

@bot.message_handler(func=lambda m: True)
def handle_message(m):
    try:
        # Уточняем роль для ИИ, чтобы избежать ошибок региона через промпт
        full_prompt = f"Ты - Директор Системы, созданный Климентом. Отвечай как продвинутый ИИ. Приказ: {m.text}"
        response = model.generate_content(full_prompt)
        
        if response.text:
            bot.reply_to(m, response.text)
        else:
            bot.reply_to(m, "Ядро зафиксировало пустой ответ. Повторите запрос.")
            
    except Exception as e:
        logger.error(f"Ошибка Gemini: {e}")
        bot.reply_to(m, f"⚠️ Сбой связи с ядром. Причина: {str(e)[:50]}")

if __name__ == "__main__":
    boot_sequence()
    # Запуск сервера
    app.run(host="0.0.0.0", port=10000)
