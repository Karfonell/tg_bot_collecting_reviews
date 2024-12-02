from buttons import back_button
from functions.message_to_support import message_to_support


def describe_problem(bot, message):
    bot.send_message(message.chat.id, 'Опишите пожалуйста свою проблему', reply_markup=back_button)
    bot.register_next_step_handler(message, lambda msg: message_to_support(bot, msg))