from buttons import contact_buttons


def get_contact(bot, message, user_problem, message_id):
    bot.send_message(message.chat.id, 'Для отправки вашего сообщения, поделитесь пожалуйста контактом',
                     reply_markup=contact_buttons)
    from functions.processing_contact import processing_contact
    bot.register_next_step_handler(message, lambda msg:processing_contact(bot, msg, user_problem, message_id))