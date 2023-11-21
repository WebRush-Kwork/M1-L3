import telebot
from config import token

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Я бот для управления чатом 😌")


@bot.message_handler(commands=['ban'])
def ban_user(message):
    if message.reply_to_message:
        chat_id = message.chat.id
        user_id = message.reply_to_message.from_user.id
        user_status = bot.get_chat_member(chat_id, user_id).status
        if user_status == 'administrator' or user_status == 'creator':
            bot.reply_to(message, "Невозможно забанить администратора 👨‍💻")
        else:
            bot.ban_chat_member(chat_id, user_id)
            bot.reply_to(
                message, f"Пользователь @{message.reply_to_message.from_user.username} был забанен 🥰")
    else:
        bot.reply_to(
            message, "Эта команда должна быть использована в ответ на сообщение пользователя, которого вы хотите забанить 🧐")


@bot.message_handler(func=lambda message: "бот" and "плохой" in message.text.lower())
def handle_message(message):
    try:
        bot.ban_chat_member(message.chat.id, message.from_user.id)
        bot.reply_to(
            message, f"Пользователь @{message.reply_to_message.from_user.username} был забанен 🥰")
    except:
        bot.reply_to(message, "Забанил бы тебя, но ты админ 😡")


bot.infinity_polling(none_stop=True)
