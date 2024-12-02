import telebot
import os
from dotenv import load_dotenv
from functions.start import start


load_dotenv('token.env')
bot = telebot.TeleBot(os.getenv('TELEGRAM_BOT_TOKEN'))

@bot.message_handler(commands=['start'])
def handle_start(message):
    start(bot, message)
bot.polling(none_stop=True)

