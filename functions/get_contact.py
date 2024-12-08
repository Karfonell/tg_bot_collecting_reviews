from buttons import contact_buttons
from database.log_to_db import log_to_db


def get_contact(bot, message, user_problem, message_id):
    bot_message = bot.send_message(message.chat.id, 'Для отправки вашего сообщения, поделитесь пожалуйста контактом',
                     reply_markup=contact_buttons)
    log_to_db(bot_message, 'get_contact', 'Сообщение от бота')
    from functions.processing_contact import processing_contact
    bot.register_next_step_handler(message, lambda msg:processing_contact(bot, msg, user_problem, message_id))