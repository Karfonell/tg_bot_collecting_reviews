from buttons import back_button
from functions.message_to_support import message_to_support
from database.log_to_db import log_to_db


def describe_problem(bot, message):
    bot_message = bot.send_message(message.chat.id, 'Опишите пожалуйста свою проблему', reply_markup=back_button)
    log_to_db(bot_message, 'describe_problem', 'Сообщение от бота')
    bot.register_next_step_handler(message, lambda msg: message_to_support(bot, msg))