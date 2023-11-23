import telebot
from config import token

bot = telebot.TeleBot(token)


def get_banned_users():
    try:
        with open('banned_users.txt', 'r') as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return []


banned_users = get_banned_users()


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Привет! Я бот для управления чатом 😌')


@bot.message_handler(commands=['info'])
def info(message):
    caption = 'Итак, я бот для бана нехороших пользователей!\nИспользуй весь мой функционал путем нажатия на кнопку с командами! 💻'
    with open('images/commands.png', 'rb') as photo:
        bot.send_photo(message.chat.id, photo, caption=caption)


@bot.message_handler(commands=['ban'])
def ban_user(message):
    global banned_users
    if message.reply_to_message:
        chat_id = message.chat.id
        user_id = message.reply_to_message.from_user.id
        user_status = bot.get_chat_member(chat_id, user_id).status
        if user_status == 'administrator' or user_status == 'creator':
            bot.reply_to(message, 'Невозможно забанить администратора 👨‍💻')
        else:
            try:
                with open('banned_users.txt', 'r') as file:
                    banned_users = file.read().splitlines()
            except FileNotFoundError:
                with open('banned_users.txt', 'w') as file:
                    file.write('')
            user_name = message.reply_to_message.from_user.username
            bot.ban_chat_member(chat_id, user_id)
            if user_name not in banned_users:
                with open('banned_users.txt', 'a') as file:
                    file.write(user_name + '\n')
                bot.reply_to(
                    message, f'Пользователь @{user_name} был забанен 🥰')
            else:
                bot.reply_to(
                    message, f'Пользователь @{user_name} уже был забанен ранее 🫢')
    else:
        bot.reply_to(
            message, 'Эта команда должна быть использована в ответ на сообщение пользователя, которого вы хотите забанить 🧐')


@bot.message_handler(commands=['list'])
def list_users(message):
    banned_users = get_banned_users()
    if banned_users:
        users_list = '\n'.join(f'@{user}' for user in banned_users)
        bot.reply_to(
            message, f'Список забаненных пользователей 👨‍💻:\n{users_list}')
    else:
        bot.reply_to(message, 'Список забаненных пользователей пуст ✅')


@bot.message_handler(func=lambda message: 'бот' and 'плохой' in message.text.lower())
def handle_message(message):
    user_id = message.from_user.id
    user_name = message.from_user.username
    if user_name not in banned_users:
        try:
            bot.ban_chat_member(message.chat.id, user_id)
            with open('banned_users.txt', 'a') as file:
                file.write(user_name + '\n')
            bot.reply_to(
                message, f'Пользователь @{user_name} был забанен 🥰')
        except:
            bot.reply_to(message, 'Забанил бы тебя, но ты админ 😡')
    else:
        bot.reply_to(
            message, f'Пользователь @{user_name} уже был забанен ранее 🫢')


bot.infinity_polling(none_stop=True)
