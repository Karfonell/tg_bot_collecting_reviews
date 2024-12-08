from database.database_conection import connect_db
import mysql.connector

def log_cursor_to_db(message_id, chat_id, username, text_message, function, action):
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
