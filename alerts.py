import time
import threading
from telebot import TeleBot
from scanner import compare_all_exchanges

API_TOKEN = '8065004819:AAGCuaB5ImkIPHqQKp4alsX4ue9GFvpqt-4'
bot = TeleBot(API_TOKEN)

# Замените на список ваших VIP-пользователей (или подключите базу)
vip_users = ["7833365313"]

# Функция авторассылки
def send_alerts():
    while True:
        try:
            results = compare_all_exchanges()
            if any("Profit:" in r or "💰" in r for r in results):
                message = "🔔 <b>Новая связка:</b>\n\n" + "\n".join(results[:2])
                for uid in vip_users:
                    bot.send_message(uid, message, parse_mode="HTML")
            time.sleep(600)  # каждые 10 минут
        except Exception as e:
            print("Alert error:", e)
            time.sleep(300)

# Запуск в отдельном потоке
def start_alert_thread():
    t = threading.Thread(target=send_alerts)
    t.daemon = True
    t.start()
