from buttons import back_button, bad_review_buttons
from database.log_to_db import log_to_db

def bad_review_retrying(bot, message):
    log_to_db(message, 'bad_review_retrying', 'Сообщение от пользователя')
    if message.text == 'Назад':
        from functions.start import start
        start(bot, message)
    elif message.text == 'Отправить еще раз':
        bot_message = bot.send_message(message.chat.id, 'Пожалуйста, отправьте скриншот своего отзыва', reply_markup=back_button)
        log_to_db(bot_message, 'bad_review_retrying', 'Сообщение от  бота')

        from functions.screenshot_processing import screenshot_processing
        bot.register_next_step_handler(message, lambda msg: screenshot_processing(bot, msg))
    else:
        bot_message = bot.send_message(message.chat.id, 'Пожалуйста, воспользуйтесь кнопками',
                         reply_markup=bad_review_buttons)
        log_to_db(bot_message, 'bad_review_retrying', 'Сообщение от бота')

        bot.register_next_step_handler(message, lambda msg:bad_review_retrying(bot, msg))