import telebot
from telebot import types

bot = telebot.TeleBot('7509475025:AAHewNKEJLhFqno5SbWu1cv0YY2eDhlGPmE')

start_buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)
bt_bonus = types.KeyboardButton('Хочу бонус!')
bt_support = types.KeyboardButton('Обращение в техподдержку')
start_buttons.add(bt_bonus)
start_buttons.add(bt_support)

back_button = types.ReplyKeyboardMarkup(resize_keyboard=True)
bt_back = types.KeyboardButton('Назад')
back_button.add(bt_back)

contact_buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)
bt_contact = types.KeyboardButton('Поделиться контактом', request_contact=True)
contact_buttons.add(bt_contact)
contact_buttons.add(bt_back)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'По какому поводу вы к нам обратились?', reply_markup=start_buttons)

    bot.register_next_step_handler(message, purpose_bot_using)

def purpose_bot_using(message):
    if message.text == 'Хочу бонус!':
        bot.send_message(message.chat.id, 'доделать', reply_markup=back_button) #доделать
    elif message.text == 'Обращение в техподдержку':
        describe_problem(message)

def describe_problem(message):
        bot.send_message(message.chat.id, 'Опишите пожалуйста свою проблему', reply_markup=back_button)
        bot.register_next_step_handler(message, message_to_support)

def message_to_support(message):
    if message.text == 'Назад':
        start(message)
    else:
        user_problem = message.text
        get_contact(message)

def get_contact(message):
    bot.send_message(message.chat.id, 'Для отправки вашего сообщения, поделитесь пожалуйста контактом',
                     reply_markup=contact_buttons)
    bot.register_next_step_handler(message, processing_contact)

def processing_contact(message):
    if message.text == 'Назад':
        describe_problem(message)
    else:
        contact = message.contact
        bot.send_message(message.chat.id, 'Передали ваше обращение в поддержку', reply_markup=start_buttons)
        bot.register_next_step_handler(message, purpose_bot_using)
bot.polling(none_stop=True)

