from telebot import types

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
bad_review_buttons.add(bt_retry)
bad_review_buttons.add(bt_back)

bt_back_back = types.KeyboardButton('Назад')