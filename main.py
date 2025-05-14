import telebot
from telebot import types
import json
from datetime import datetime
from scanner import compare_all_exchanges
from spot_arb import compare_tokens
from memecoins import compare_memecoins
from alerts import start_alert_thread

API_TOKEN = '8065004819:AAFLL7_Hmso6nysO0hqS4ga9EnWPuPLWewg'
bot = telebot.TeleBot(API_TOKEN)
start_alert_thread()

try:
    with open("vip_users.json", "r") as f:
        vip_users = json.load(f)
except:
    vip_users = {}

def save_vip():
    with open("vip_users.json", "w") as f:
        json.dump(vip_users, f)

def check_access(user_id, level):
    access = {
        "Basic": ["P2P"],
        "Pro": ["P2P", "Spot"],
        "Expert": ["P2P", "Spot", "Memecoins", "Alerts"]
    }
    current = vip_users.get(str(user_id), {}).get("level", "Basic")
    return level in access.get(current, [])

main_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add("🔁 P2P", "📊 Spot", "🐸 Мемкойны")
main_menu.add("📈 Калькулятор", "💎 Подписка", "👤 Мой ID", "📘 Помощь")

@bot.message_handler(commands=['start'])
def start(message):
    name = message.from_user.first_name or "друг"
    bot.send_message(message.chat.id, f"👋 Привет, <b>{name}</b>! Это P2P SCANNER BOT.", parse_mode="HTML", reply_markup=main_menu)

@bot.message_handler(func=lambda msg: msg.text == "🔁 P2P")
def p2p_handler(message):
    if check_access(message.chat.id, "P2P"):
        results = compare_all_exchanges()
        bot.send_message(message.chat.id, "\n".join(results))
    else:
        bot.send_message(message.chat.id, "🔒 Недоступно. Ваш уровень подписки: только Basic.")

@bot.message_handler(func=lambda msg: msg.text == "📊 Spot")
def spot_handler(message):
    if check_access(message.chat.id, "Spot"):
        results = compare_tokens()
        bot.send_message(message.chat.id, "\n".join(results))
    else:
        bot.send_message(message.chat.id, "🔒 Spot-доступ только с уровнем Pro и выше.")

@bot.message_handler(func=lambda msg: msg.text == "🐸 Мемкойны")
def meme_handler(message):
    if check_access(message.chat.id, "Memecoins"):
        results = compare_memecoins()
        bot.send_message(message.chat.id, "\n".join(results))
    else:
        bot.send_message(message.chat.id, "🔒 Мемкойны доступны только на уровне Expert.")

@bot.message_handler(func=lambda msg: msg.text == "📈 Калькулятор")
def calculator(message):
    msg = bot.send_message(message.chat.id, "📊 Введите дневной % (например, 1.2):")
    bot.register_next_step_handler(msg, process_percent)

def process_percent(message):
    try:
        percent = float(message.text.strip())
        msg = bot.send_message(message.chat.id, "📆 На сколько дней рассчитать?")
        bot.register_next_step_handler(msg, lambda m: process_days(m, percent))
    except:
        bot.send_message(message.chat.id, "❌ Введите число.")

def process_days(message, percent):
    try:
        days = int(message.text.strip())
        start = 1000
        final = start * (1 + percent / 100) ** days
        bot.send_message(message.chat.id,
                         f"📈 Начальная сумма: $1000\n📉 Дневной %: {percent}%\n📆 Дней: {days}\n\n💰 Итог: <b>${final:.2f}</b>",
                         parse_mode="HTML")
    except:
        bot.send_message(message.chat.id, "❌ Введите целое число дней.")

@bot.message_handler(func=lambda msg: msg.text == "💎 Подписка")
def subscribe_info(message):
    bot.send_message(message.chat.id,
        "💎 Уровни подписки:\n"
        "🔹 Basic — только P2P (бесплатно)\n"
        "🔸 Pro — Spot, $5 в месяц\n"
        "🔶 Expert — Всё: мемкойны, алерты, отчёты ($10/мес)\n\n"
        "👤 Свяжитесь с админом для активации: @P2p_sng_bot", parse_mode="HTML")

@bot.message_handler(func=lambda msg: msg.text == "👤 Мой ID")
def show_profile(message):
    uid = str(message.chat.id)
    level = vip_users.get(uid, {}).get("level", "Basic")
    bot.send_message(message.chat.id, f"🧾 Ваш ID: <code>{uid}</code>\nУровень: <b>{level}</b>", parse_mode="HTML")

@bot.message_handler(func=lambda msg: msg.text == "📘 Помощь")
def help_command(message):
    bot.send_message(message.chat.id,
        "📘 Команды:\n"
        "🔁 P2P — выгодные связки USDT по USD\n"
        "📊 Spot — арбитраж BTC/ETH/DOGE\n"
        "🐸 Мемкойны — сравнение PEPE, SHIB, FLOKI\n"
        "📈 Калькулятор — сложный процент\n"
        "👤 Мой ID — статус подписки\n\n"
        "❓ Вопросы? Пиши: @P2p_sng_bot", parse_mode="HTML")

bot.polling(none_stop=True)
