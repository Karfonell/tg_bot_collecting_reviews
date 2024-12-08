from database.database_conection import connect_db
import mysql.connector

def log_to_db(message, function, action):
    message_id = message.message_id
    chat_id = message.chat.id
    username = message.from_user.username
    text_message = message.text if message.text else message.caption

    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            query = "INSERT INTO logs (message_id, chat_id, username, message, `function`, action) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (message_id, chat_id, username, text_message, function, action))
            conn.commit()
        except mysql.connector.Error as e:
            print(f"Ошибка записи в базу данных: {e}")
        finally:
            cursor.close()
            conn.close()
