from buttons import review_buttons, back_button
from telebot import types
import os
from dotenv import load_dotenv
import mysql.connector
from database.log_to_db import log_to_db
from database.log_img_to_db import log_img_to_db
from database.database_conection import connect_db
from database.log_cursor_to_db import log_cursor_to_db


def screenshot_processing(bot, message):
    load_dotenv('token.env')
    admin_id = os.getenv('ADMIN_CHAT_ID')
    if message.text == 'Назад':
        log_to_db(message, 'screenshot_processing', 'Сообщение от пользователя')
        from functions.start import start
        start(bot, message)

    elif message.content_type == 'photo':
        bot_message = bot.send_message(message.chat.id,
                         'Отправленное изображение находится на модерации.\n'
                         'Пожалуйста, подождите, мы скоро вам ответим!\n'
                         'До момента ответа нашего модератора работа бота будет приостановлена',
                         reply_markup=types.ReplyKeyboardRemove())

        photo_id = message.photo[-1].file_id
        file_info = bot.get_file(photo_id)
        file = bot.download_file(file_info.file_path)
        log_img_to_db(bot, message, 'screenshot_processing', 'Сохранение изображения')
        log_to_db(bot_message, 'screenshot_processing', 'Сообщение от бота')
        message_admin = bot.send_photo(admin_id,
                                       file,
                                       caption='Оцените отзыв',
                                       reply_markup=review_buttons)
        log_to_db(message_admin, 'screenshot_processing', 'Сообщение администратору')

        conn = connect_db()
        if conn:
            try:
                cursor = conn.cursor()
                query = "INSERT INTO reviews (id_review, id_chat_user, is_checked) VALUES (%s, %s, %s)"
                cursor.execute(query, (message_admin.id, message.chat.id, 0))
                conn.commit()
                log_cursor_to_db(message.message_id,
                                 message.chat.id,
                                 message.from_user.username,
                                 "Удачная попытка добавления записи в таблицу reviews",
                                 'screenshot_processing',
                                 'Работа с базой данных')
            except mysql.connector.Error as e:
                log_cursor_to_db(message.message_id,
                                 message.chat.id,
                                 message.from_user.username,
                                 f"Ошибка записи в таблицу reviews: {e}",
                                 'screenshot_processing',
                                 'Ошибка в работе с базой данных')
            finally:
                cursor.close()
                conn.close()

        from functions.review_processed import review_processed
        bot.register_next_step_handler(message_admin, lambda msg: review_processed(msg, message, bot))
    else:
        bot_message = bot.send_message(message.chat.id,
                                       'Пожалуйста, отправьте скриншот своего отзыва',
                                       reply_markup=back_button)
        log_to_db(bot_message, 'purpose_bot_using', 'Сообщение от бота')

        bot.register_next_step_handler(message, lambda msg: screenshot_processing(bot, msg))