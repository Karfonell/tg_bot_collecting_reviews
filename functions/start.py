from buttons import start_buttons


def start(bot, message):
    bot.send_message(message.chat.id, 'По какому поводу вы к нам обратились?', reply_markup=start_buttons)

    from functions.purpose_bot_using import purpose_bot_using
    bot.register_next_step_handler(message, lambda msg: purpose_bot_using(bot, msg))