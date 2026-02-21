import telebot
import requests
import os
from flask import Flask
from threading import Thread
import time

# 1. Получаем ключи из секретов Render
TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_KEY = os.environ.get("GEMINI_KEY")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# --- МОДУЛИ СИСТЕМЫ ---

def oracle_process():
    """Модуль Оракул - фоновый анализ"""
    print("--- ORACLE ONLINE ---")
    while True:
        time.sleep(3600)

def sentinel_process():
    """Модуль Сентинел - защита и мониторинг"""
    print("--- SENTINEL ONLINE ---")
    while True:
        time.sleep(3600)

# --- ЛОГИКА ДИРЕКТОРА (ИИ) ---

@bot.message_handler(func=lambda m: True)
def chat(m):
    if not GEMINI_KEY:
        bot.reply_to(m, "Ошибка: Ключ GEMINI_KEY не задан в настройках Render.")
        return

    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [{
            "parts": [{"text": "Ты Директор системы Империя. Отвечай кратко и властно: " + m.text}]
        }]
    }
    
    try:
        r = requests.post(url, json=data, headers=headers, timeout=30)
        res = r.json()
        if 'candidates' in res:
            text = res['candidates'][0]['content']['parts'][0]['text']
            bot.reply_to(m, text)
        else:
            bot.reply_to(m, "Ядро ИИ временно недоступно.")
    except Exception as e:
        bot.reply_to(m, "Сбой связи с командным центром.")

# --- ВЕБ-ИНТЕРФЕЙС ДЛЯ RENDER ---

@app.route('/')
def home():
    return "Empire System Status: DIRECTOR, ORACLE, SENTINEL ARE ACTIVE."

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# --- ТОЧКА ЗАПУСКА ---

if name == "__main__":
    # Запуск Веб-сервера (чтобы Render видел, что мы живы)
    Thread(target=run_web, daemon=True).start()
    
    # Запуск Оракула и Сентинела (как ты и просил - автостарт)
    Thread(target=oracle_process, daemon=True).start()
    Thread(target=sentinel_process, daemon=True).start()
    
    print("--- СИСТЕМА ИМПЕРИЯ ПОЛНОСТЬЮ ЗАПУЩЕНА ---")
    
    # Запуск Бота (Директор)
    bot.remove_webhook()
    bot.infinity_polling()
