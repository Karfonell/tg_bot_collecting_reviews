import telebot
import os
from telebot import types
from dotenv import load_dotenv

load_dotenv('token.env')
admin_id = os.getenv('ADMIN_CHAT_ID')

user_problems = {}
waiting_for_review = {}


bot = telebot.TeleBot(os.getenv('TELEGRAM_BOT_TOKEN'))

start_buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)
bt_bonus = types.KeyboardButton('Хочу бонус!')
bt_support = types.KeyboardButton('Обращение в техподдержку')
start_buttons.add(bt_bonus)
start_buttons.add(bt_support)

back_button = types.ReplyKeyboardMarkup(resize_keyboard=True)
bt_back = types.KeyboardButton('Назад')
back_button.add(bt_back)

contact_buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)
bt_contact = types.KeyboardButton('Поделиться контактом', request_contact=True)
contact_buttons.add(bt_contact)
contact_buttons.add(bt_back)

review_buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)
bt_good_review = types.KeyboardButton('Отзыв подходит')
bt_bad_review = types.KeyboardButton('Отзыв не подходит')
review_buttons.add(bt_good_review)
review_buttons.add(bt_bad_review)

bad_review_buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)
bt_retry = types.KeyboardButton('Отправить еще раз')
bt_back = types.KeyboardButton('Назад')
bad_review_buttons.add(bt_retry)
bad_review_buttons.add(bt_back)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'По какому поводу вы к нам обратились?', reply_markup=start_buttons)

    bot.register_next_step_handler(message, purpose_bot_using)

def purpose_bot_using(message):
    if message.text == 'Хочу бонус!':
        instruction = (
                    'Пожалуйста, отправьте скриншот из раздела покупок для идентификации товара и получения бонуса.' +
                    '\n- Вам необходимо зайти на сайт wildberries.ru (https://www.wildberries.ru/) или в мобильное ' +
                    'приложение и авторизоваться по номеру вашего телефона;- Нажать на «Профиль»;' +
                    '\n- Выбрать раздел «Покупки»;\n- Сделать скриншот, где будет видно что вы приобрели наш товар')
        bot.send_message(message.chat.id, instruction, reply_markup=back_button)
        bot.register_next_step_handler(message, screenshot_processing)
    elif message.text == 'Обращение в техподдержку':
        describe_problem(message)
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, воспользуйтесь кнопками', reply_markup=start_buttons)
        bot.register_next_step_handler(message, purpose_bot_using)

def describe_problem(message):
        bot.send_message(message.chat.id, 'Опишите пожалуйста свою проблему', reply_markup=back_button)
        bot.register_next_step_handler(message, message_to_support)

def message_to_support(message):
    if message.text == 'Назад':
        start(message)
    else:
        user_problem = message.text
        user_problems[message.chat.id] = user_problem
        get_contact(message)

def get_contact(message):
    bot.send_message(message.chat.id, 'Для отправки вашего сообщения, поделитесь пожалуйста контактом',
                     reply_markup=contact_buttons)
    bot.register_next_step_handler(message, processing_contact)

def processing_contact(message):
    if message.text == 'Назад':
        describe_problem(message)
    elif message.contact:
        contact = message.contact
        user_problem = user_problems.get(message.chat.id, "Проблема не указана")
        bot.send_message(
            admin_id,
            f"Телефон: {contact.phone_number}\n"
            f"Обращение: {user_problem}"
        )
        bot.send_message(message.chat.id, 'Передали ваше обращение в поддержку', reply_markup=start_buttons)
        bot.register_next_step_handler(message, purpose_bot_using)
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, отправьте корректные данные', reply_markup=contact_buttons)
        bot.register_next_step_handler(message, processing_contact)

def screenshot_processing(message):
    if message.text == 'Назад':
        start(message)
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
        waiting_for_review[message_admin.id] = message.chat.id
        bot.register_next_step_handler(message_admin, lambda msg: review_processed(msg, message))
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, отправьте скриншот своего отзыва', reply_markup=back_button)
        bot.register_next_step_handler(message, screenshot_processing)

def review_processed(message_admin, message):
    replied_message_admin_id = message_admin.reply_to_message.message_id

    user_message_chat_id = waiting_for_review.pop(replied_message_admin_id, None)

    if user_message_chat_id == message.chat.id:

        if message_admin.text == 'Отзыв подходит':
            good_review_message = 'Спасибо за отзыв! Дарим вам расширенную гарантию сроком на 12 месяцев!\n'\
                                   "Ваш код расширенной гарантии - 8605321373223\n"\
                                   "Если у вас возникнут проблемы с товаром в течение 12 месяцев или другой вопрос, "\
                                   "просто напишите нам в этот чат"
            bot.send_message(message.chat.id, good_review_message, reply_markup=start_buttons)
            bot.register_next_step_handler(message, purpose_bot_using)
        elif message_admin.text == 'Отзыв не подходит':
            bad_review_message = 'К сожалению, это изображение не подходит для получения бонуса😔\n'\
                                     'Для его получения вам требуется:\n'\
                                     '- Зайти на сайт wildberries.ru (https://www.wildberries.ru/) или в мобильное приложение '\
                                     'и авторизоваться по номеру вашего телефона;\n'\
                                     '- Нажать на «Профиль»;\n'\
                                     '- Выбрать раздел «Покупки»;\n'\
                                     '- Сделать скриншот, где будет видно что вы приобрели наш товар\n'
            bot.send_message(message.chat.id, bad_review_message, reply_markup=bad_review_buttons)
            bot.register_next_step_handler(message, bad_review_retrying)
        else:
            bot.send_message(message_admin.chat.id, 'Пожалуйста, нажмите на одну из кнопок', reply_markup=review_buttons)
            bot.register_next_step_handler(message_admin, lambda msg: review_processed(msg, message))
    else:
        bot.register_next_step_handler(message_admin, lambda msg: review_processed(msg, message))

def bad_review_retrying(message):
    if message.text == 'Назад':
        start(message)
    elif message.text == 'Отправить еще раз':
        bot.send_message(message.chat.id, 'Пожалуйста, отправьте скриншот своего отзыва',
                         reply_markup=bt_back)
        bot.register_next_step_handler(message, screenshot_processing)
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, воспользуйтесь кнопками',
                         reply_markup=bad_review_buttons)
        bot.register_next_step_handler(message, bad_review_retrying)


bot.polling(none_stop=True)

