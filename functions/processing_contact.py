import mysql.connector
from database.database_conection import connect_db
from buttons import start_buttons, contact_buttons
from dotenv import load_dotenv
import os
from database.log_to_db import log_to_db
from database.log_cursor_to_db import log_cursor_to_db


def processing_contact(bot, message, user_problem, message_id):
    log_to_db(message, 'processing_contact', 'Сообщение от пользователя')
    if message.text == 'Назад':
        from functions.describe_problem import describe_problem
        describe_problem(bot, message)

    elif message.contact:
        contact = message.contact

        conn = connect_db()
        if conn:
            try:
                cursor = conn.cursor()
                query = "INSERT INTO troubles (chat_id, message_id, user_problem, contact) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, (message.chat.id, message.message_id, user_problem, contact.phone_number))
                conn.commit()
                log_cursor_to_db(message.message_id,
                                 message.chat.id,
                                 message.from_user.username,
                                 "Удачная запись в таблицу troubles",
                                 'processing_contact',
                                 'Работа с базой данных')

            except mysql.connector.Error as e:
                log_cursor_to_db(message.message_id,
                                 message.chat.id,
                                message.from_user.username,
                                 f"Ошибка записи в таблицу troubles: {e}",
                                 'processing_contact',
                                 'Ошибка в работе с базой данных')
            finally:
                cursor.close()
                conn.close()

        load_dotenv('token.env')
        admin_id = os.getenv('ADMIN_CHAT_ID')
        admin_message = bot.send_message(
            admin_id,
            f"Телефон: {contact.phone_number}\n"
            f"Обращение: {user_problem}"
        )
        log_to_db(admin_message, 'processing_contact', 'Сообщение администратору')

        bot_message = bot.send_message(message.chat.id, 'Передали ваше обращение в поддержку',
                                       reply_markup=start_buttons)
        log_to_db(bot_message, 'processing_contact', 'Сообщение от бота')

        from functions.purpose_bot_using import purpose_bot_using
        bot.register_next_step_handler(message, lambda msg: purpose_bot_using(bot, msg))
    else:
        bot_message = bot.send_message(message.chat.id, 'Пожалуйста, отправьте корректные данные',
                                       reply_markup=contact_buttons)
        log_to_db(bot_message, 'processing_contact', 'Сообщение от бота')
        bot.register_next_step_handler(message, lambda msg:processing_contact(bot, msg, user_problem, message_id))