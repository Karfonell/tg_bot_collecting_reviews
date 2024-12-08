from buttons import start_buttons
from database.log_to_db import log_to_db


def start(bot, message):
    log_to_db(message, 'start', 'Сообщение от пользователя')
    bot_message = bot.send_message(message.chat.id, 'По какому поводу вы к нам обратились?', reply_markup=start_buttons)
    log_to_db(bot_message, 'start', 'Сообщение от бота')
    from functions.purpose_bot_using import purpose_bot_using
    bot.register_next_step_handler(message, lambda msg: purpose_bot_using(bot, msg))