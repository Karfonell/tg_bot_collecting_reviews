import random
import mysql.connector
from database.log_to_db import log_to_db
from database.database_conection import connect_db
from database.log_cursor_to_db import log_cursor_to_db
from buttons import review_buttons, start_buttons, bad_review_buttons

def review_processed(message_admin, message, bot):
    log_to_db(message_admin, 'review_processed', 'Сообщение администратора')
    if message_admin.reply_to_message:
        replied_message_admin_id = message_admin.reply_to_message.message_id
    else:
        replied_message_admin_id = 0

    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            query = "SELECT id_chat_user FROM reviews WHERE id_review = %s LIMIT 1"
            cursor.execute(query, (replied_message_admin_id,))
            result = cursor.fetchone()

            if result:
                user_message_chat_id = result[0]
            else:
                user_message_chat_id = None
            conn.commit()
            log_cursor_to_db(message_admin.message_id,
                             message_admin.chat.id,
                             message_admin.from_user.username,
                             "Удачная попытка чтения таблицы reviews",
                             'review_processed',
                             'Работа с базой данных')
        except mysql.connector.Error as e:
            log_cursor_to_db(message_admin.message_id,
                             message_admin.chat.id,
                             message_admin.from_user.username,
                             f"Ошибка чтения таблицы reviews: {e}",
                             'review_processed',
                             'Ошибка в работе с базой данных')
        finally:
            cursor.close()
            conn.close()

    if user_message_chat_id == message.chat.id:
        if message_admin.text == 'Отзыв подходит':
            conn = connect_db()
            if conn:
                try:
                    cursor = conn.cursor()
                    update_query = """
                                UPDATE reviews 
                                SET is_checked = %s, is_good_review = %s 
                                WHERE id_review = %s
                            """
                    cursor.execute(update_query, (1, 1, replied_message_admin_id))
                    conn.commit()
                    log_cursor_to_db(message_admin.message_id,
                                     message_admin.chat.id,
                                     message_admin.from_user.username,
                                     f"Удачное обновление таблицы reviews",
                                     'review_processed',
                                     'Работа с базой данных')
                except mysql.connector.Error as e:
                    log_cursor_to_db(message_admin.message_id,
                                     message_admin.chat.id,
                                     message_admin.from_user.username,
                                     f"Ошибка обновления таблицы reviews: {e}",
                                     'review_processed',
                                     'Ошибка в работе с базой данных')
                finally:
                    cursor.close()
                    conn.close()

            guarantee = random.randint(10 ** 14, 10 ** 15 - 1)
            good_review_message = 'Спасибо за отзыв! Дарим вам расширенную гарантию сроком на 12 месяцев!\n'\
                                   f"Ваш код расширенной гарантии - {guarantee}\n"\
                                   "Если у вас возникнут проблемы с товаром в течение 12 месяцев или другой вопрос, "\
                                   "просто напишите нам в этот чат"
            bot_message = bot.send_message(message.chat.id, good_review_message, reply_markup=start_buttons)
            log_to_db(bot_message, 'review_processed', 'Сообщение от бота')

            from functions.purpose_bot_using import purpose_bot_using
            bot.register_next_step_handler(message, lambda msg: purpose_bot_using(bot, msg))
        elif message_admin.text == 'Отзыв не подходит':

            conn = connect_db()
            if conn:
                try:
                    cursor = conn.cursor()
                    update_query = """
                                            UPDATE reviews 
                                            SET is_checked = %s, is_good_review = %s 
                                            WHERE id_review = %s
                                        """
                    cursor.execute(update_query, (1, 0, replied_message_admin_id))
                    conn.commit()
                    log_cursor_to_db(message_admin.message_id,
                                     message_admin.chat.id,
                                     message_admin.from_user.username,
                                     "Удачная попытка обновления таблицы reviews",
                                     'review_processed',
                                     'Работа с базой данных')
                except mysql.connector.Error as e:
                    log_cursor_to_db(message_admin.message_id,
                                     message_admin.chat.id,
                                     message_admin.from_user.username,
                                     f"Ошибка обновления таблицы reviews: {e}",
                                     'review_processed',
                                     'Ошибка в работе с базой данных')
                finally:
                    cursor.close()
                    conn.close()

            bad_review_message = 'К сожалению, это изображение не подходит для получения бонуса\n'\
                                     'Для его получения вам требуется:\n'\
                                     '- Зайти на сайт wildberries.ru (https://www.wildberries.ru/) или в мобильное приложение '\
                                     'и авторизоваться по номеру вашего телефона;\n'\
                                     '- Нажать на «Профиль»;\n'\
                                     '- Выбрать раздел «Покупки»;\n'\
                                     '- Сделать скриншот, где будет видно что вы приобрели наш товар\n'
            bot_message = bot.send_message(message.chat.id, bad_review_message, reply_markup=bad_review_buttons)
            log_to_db(bot_message, 'review_processed', 'Сообщение от бота')

            from functions.bad_review_retrying import bad_review_retrying
            bot.register_next_step_handler(message, lambda msg: bad_review_retrying(bot, msg))
        else:
            bot_message = bot.send_message(message_admin.chat.id,
                                           'Пожалуйста, нажмите на одну из кнопок',
                                           reply_markup=review_buttons)
            log_to_db(bot_message, 'review_processed', 'Сообщение от бота')
            bot.register_next_step_handler(message_admin, lambda msg: review_processed(msg, message, bot))
    else:
        bot.register_next_step_handler(message_admin, lambda msg: review_processed(msg, message, bot))
