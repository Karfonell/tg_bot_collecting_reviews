def message_to_support(bot, message):
    if message.text == 'Назад':
        from functions.start import start
        start(bot, message)
    else:
        user_problem = message.text

        from functions.get_contact import get_contact
        get_contact(bot, message, user_problem, message.message_id)