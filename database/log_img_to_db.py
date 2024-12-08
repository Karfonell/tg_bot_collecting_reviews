import os
from dotenv import load_dotenv
from database.database_conection import connect_db
import mysql.connector


def log_img_to_db(bot, message, function, action) :
    message_id = message.message_id
    chat_id = message.chat.id
    username = message.from_user.username

    load_dotenv('token.env')
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER')
    photo_id = message.photo[-1].file_id
    file_info = bot.get_file(photo_id)
    downloaded_file = bot.download_file(file_info.file_path)
    file_path = os.path.join(UPLOAD_FOLDER, f"{message_id}.jpg")

    with open(file_path, 'wb') as photo_file:
        photo_file.write(downloaded_file)

    text_message = file_path

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