import os
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

# Render soxta HTTP serveri (Port xatosi bermasligi uchun)
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive!")

def run_health_check_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    server.serve_forever()

# Bot tokeni va Mini App manzili
TOKEN = "8831876122:AAG_A9zvffr_CwrvoTYYvM9njRegWIh1UwI"
WEBAPP_URL = "https://abduraxmonlatifjonov4126-web.github.io/My-vocab/"

# Oddiy va barqaror TeleBot (async xatolarisiz)
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    first_name = message.from_user.first_name
    
    # Inline tugma va WebAppInfo (to_dict xatosini bartaraf etadi)
    markup = InlineKeyboardMarkup()
    app_button = InlineKeyboardButton(
        text="🚀 AUZ Vocab-ni ochish", 
        web_app=WebAppInfo(url=WEBAPP_URL)
    )
    markup.add(app_button)
    
    welcome_text = (
        f"Assalomu alaykum, {first_name}! 👋\n\n"
        f"<b>AUZ — kundalik vocab</b> botiga xush kelibsiz!\n\n"
        f"Bu yerda siz ingliz tili so'zlarini o'yinlar, fleshkartalar "
        f"va turli mashqlar orqali oson yodlashingiz mumkin.\n\n"
        f"Boshlash uchun pastdagi tugmani bosing 👇"
    )
    
    bot.send_message(
        message.chat.id, 
        welcome_text, 
        parse_mode='HTML', 
        reply_markup=markup
    )

if __name__ == "__main__":
    # Health check serverini fonda ishga tushirish
    threading.Thread(target=run_health_check_server, daemon=True).start()
    
    print("Bot muvaffaqiyatli ishga tushdi...")
    
    # Xatoliklar yuz bersa ham to'xtab qolmasligi uchun cheksiz sikl
    while True:
        try:
            bot.polling(none_stop=True, interval=1, timeout=60)
        except Exception as e:
            print(f"Xatolik yuz berdi: {e}")
            time.sleep(5)
