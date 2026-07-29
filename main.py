import os
import asyncio
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
from telebot.async_telebot import AsyncTeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Render so'rayotgan portni ochib beruvchi soxta HTTP server
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive!")

def run_health_check_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    server.serve_forever()

# Bot tokenini olish
TOKEN = os.getenv("BOT_TOKEN")
WEBAPP_URL = "https://abduraxmonlatifjonov4126-web.github.io/My-vocab/"

bot = AsyncTeleBot(TOKEN)

@bot.message_handler(commands=['start'])
async def send_welcome(message):
    first_name = message.from_user.first_name
    
    markup = InlineKeyboardMarkup()
    app_button = InlineKeyboardButton(
        text="🚀 AUZ Vocab-ni ochish", 
        web_app={'url': WEBAPP_URL}
    )
    markup.add(app_button)
    
    welcome_text = (
        f"Assalomu alaykum, {first_name}! 👋\n\n"
        f"<b>AUZ — kundalik vocab</b> botiga xush kelibsiz!\n\n"
        f"Bu yerda siz ingliz tili so'zlarini o'yinlar, fleshkartalar "
        f"va turli mashqlar orqali oson yodlashingiz mumkin.\n\n"
        f"Boshlash uchun pastdagi tugmani bosing 👇"
    )
    
    await bot.send_message(
        message.chat.id, 
        welcome_text, 
        parse_mode='HTML', 
        reply_markup=markup
    )

async def main():
    # Render uchun portni fonda yoqamiz
    threading.Thread(target=run_health_check_server, daemon=True).start()
    
    print("Bot muvaffaqiyatli ishga tushdi...")
    await bot.polling(non_stop=True)

if name == "main":
    asyncio.run(main())
