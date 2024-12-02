from buttons import review_buttons, back_button
from telebot import types
import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error
from database_conection import connect_db


def screenshot_processing(bot, message):
    load_dotenv('token.env')
    admin_id = os.getenv('ADMIN_CHAT_ID')
    if message.text == 'Назад':
        from functions.start import start
        start(bot, message)

    elif message.content_type == 'photo':
        bot.send_message(message.chat.id,
                         'Отправленное изображение находится на модерации.\n'
                         'Пожалуйста, подождите, мы скоро вам ответим!\n'
                         'До момента ответа нашего модератора работа бота будет приостановлена',
                         reply_markup=types.ReplyKeyboardRemove())
        photo_id = message.photo[-1].file_id
        file_info = bot.get_file(photo_id)
        file = bot.download_file(file_info.file_path)
        message_admin = bot.send_photo(admin_id, file, reply_markup=review_buttons)

        conn = connect_db()
        if conn:
            try:
                cursor = conn.cursor()
                query = "INSERT INTO reviews (id_review, id_chat_user, is_checked) VALUES (%s, %s, %s)"
                cursor.execute(query, (message_admin.id, message.chat.id, 0))
                conn.commit()
            except mysql.connector.Error as e:
                print(f"Ошибка записи в базу данных: {e}")
            finally:
                cursor.close()
                conn.close()

        from functions.review_processed import review_processed
        bot.register_next_step_handler(message_admin, lambda msg: review_processed(msg, message, bot))
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, отправьте скриншот своего отзыва', reply_markup=back_button)
        bot.register_next_step_handler(message, lambda msg: screenshot_processing(bot, msg))