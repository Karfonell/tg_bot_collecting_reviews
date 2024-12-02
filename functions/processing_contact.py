import mysql.connector
from mysql.connector import Error
from database_conection import connect_db
from buttons import start_buttons, contact_buttons
from dotenv import load_dotenv
import os

def processing_contact(bot, message, user_problem, message_id):
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
            except mysql.connector.Error as e:
                print(f"Ошибка записи в базу данных: {e}")
            finally:
                cursor.close()
                conn.close()

        load_dotenv('token.env')
        admin_id = os.getenv('ADMIN_CHAT_ID')
        bot.send_message(
            admin_id,
            f"Телефон: {contact.phone_number}\n"
            f"Обращение: {user_problem}"
        )


        bot.send_message(message.chat.id, 'Передали ваше обращение в поддержку', reply_markup=start_buttons)
        from functions.purpose_bot_using import purpose_bot_using
        bot.register_next_step_handler(message, lambda msg: purpose_bot_using(bot, msg))
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, отправьте корректные данные', reply_markup=contact_buttons)
        bot.register_next_step_handler(message, lambda msg:processing_contact(bot, msg, user_problem, message_id))