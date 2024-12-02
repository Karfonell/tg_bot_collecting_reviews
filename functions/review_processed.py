import mysql.connector
from mysql.connector import Error
from database_conection import connect_db
from buttons import review_buttons, start_buttons, bad_review_buttons

def review_processed(message_admin, message, bot):
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
        except mysql.connector.Error as e:
            print(f"Ошибка чтения базы данных: {e}")
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
                except mysql.connector.Error as e:
                    print(f"Ошибка обновления базы данных: {e}")
                finally:
                    cursor.close()
                    conn.close()

            good_review_message = 'Спасибо за отзыв! Дарим вам расширенную гарантию сроком на 12 месяцев!\n'\
                                   "Ваш код расширенной гарантии - 8605321373223\n"\
                                   "Если у вас возникнут проблемы с товаром в течение 12 месяцев или другой вопрос, "\
                                   "просто напишите нам в этот чат"
            bot.send_message(message.chat.id, good_review_message, reply_markup=start_buttons)

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
                except mysql.connector.Error as e:
                    print(f"Ошибка обновления базы данных: {e}")
                finally:
                    cursor.close()
                    conn.close()

            bad_review_message = 'К сожалению, это изображение не подходит для получения бонуса😔\n'\
                                     'Для его получения вам требуется:\n'\
                                     '- Зайти на сайт wildberries.ru (https://www.wildberries.ru/) или в мобильное приложение '\
                                     'и авторизоваться по номеру вашего телефона;\n'\
                                     '- Нажать на «Профиль»;\n'\
                                     '- Выбрать раздел «Покупки»;\n'\
                                     '- Сделать скриншот, где будет видно что вы приобрели наш товар\n'
            bot.send_message(message.chat.id, bad_review_message, reply_markup=bad_review_buttons)

            from functions.bad_review_retrying import bad_review_retrying
            bot.register_next_step_handler(message, lambda msg: bad_review_retrying(bot, msg))
        else:
            bot.send_message(message_admin.chat.id, 'Пожалуйста, нажмите на одну из кнопок', reply_markup=review_buttons)
            bot.register_next_step_handler(message_admin, lambda msg: review_processed(msg, message, bot))
    else:
        bot.register_next_step_handler(message_admin, lambda msg: review_processed(msg, message, bot))
