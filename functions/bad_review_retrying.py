from buttons import back_button, bad_review_buttons
from telebot import types


def bad_review_retrying(bot, message):
    if message.text == 'Назад':
        from functions.start import start
        start(bot, message)
    elif message.text == 'Отправить еще раз':
        bot.send_message(message.chat.id, 'Пожалуйста, отправьте скриншот своего отзыва', reply_markup=back_button)
        from functions.screenshot_processing import screenshot_processing
        bot.register_next_step_handler(message, lambda msg: screenshot_processing(bot, msg))
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, воспользуйтесь кнопками',
                         reply_markup=bad_review_buttons)
        bot.register_next_step_handler(message, lambda msg:bad_review_retrying(bot, msg))