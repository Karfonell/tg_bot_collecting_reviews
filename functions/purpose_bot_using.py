from buttons import start_buttons, back_button
from database.log_to_db import log_to_db

def purpose_bot_using(bot, message):
    log_to_db(message, 'purpose_bot_using', 'Сообщение от пользователя')
    if message.text == 'Хочу бонус!':
        instruction = (
                    'Пожалуйста, отправьте скриншот из раздела покупок для идентификации товара и получения бонуса.' +
                    '\n- Вам необходимо зайти на сайт wildberries.ru (https://www.wildberries.ru/) или в мобильное ' +
                    'приложение и авторизоваться по номеру вашего телефона;- Нажать на «Профиль»;' +
                    '\n- Выбрать раздел «Покупки»;\n- Сделать скриншот, где будет видно что вы приобрели наш товар')
        bot_message = bot.send_message(message.chat.id, instruction, reply_markup=back_button)
        log_to_db(bot_message, 'purpose_bot_using', 'Сообщение от бота')

        from functions.screenshot_processing import screenshot_processing
        bot.register_next_step_handler(message, lambda msg: screenshot_processing(bot, msg))

    elif message.text == 'Обращение в техподдержку':
        from functions.describe_problem import describe_problem
        describe_problem(bot, message)

    else:
        bot_message = bot.send_message(message.chat.id, 'Пожалуйста, воспользуйтесь кнопками',
                                       reply_markup=start_buttons)
        log_to_db(bot_message, 'purpose_bot_using', 'Сообщение от бота')
        bot.register_next_step_handler(message, lambda msg: purpose_bot_using(bot, msg))