import os
import asyncio
from telebot.async_telebot import AsyncTeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Bot tokenini Render muhit o'zgaruvchisidan (Environment Variable) olamiz
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
    print("Bot muvaffaqiyatli ishga tushdi...")
    await bot.polling(non_stop=True)

if __name__ == "__main__":
    asyncio.run(main())
