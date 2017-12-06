import logging

from telegram.ext import CommandHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import Updater

from bot_token import *
from order import *
from user import *


def start_command(bot, update):
    current_chat_id = update.message.chat_id
    bot.send_message(chat_id=current_chat_id,
                     text="Вас приветствует EasyDelev бот!\n"
                          "Создавайте заказы, которые вы хотите,"
                          "чтобы другие пользователи купили вам."
                          " Также не забывайте сами брать заказы других пользователей.\n"
                          "Удачи!"
                     )
    print(current_chat_id)
    add_new_user(current_chat_id)


def add_command(bot, update):
    user_id = update.message.chat_id
    set_state(user_id=user_id, state="add")


def remove_command(bot, update):
    user_id = update.message.chat_id
    delete_order(user_id)
    set_state(user_id=user_id, state="normal")
    print_orders()
    user_ids = get_users_ids(filter_id=user_id)
    for rec_id in user_ids:
        bot.send_message(chat_id=rec_id,
                         text="Заказ был удалён:\n" +
                              str(user_id))


def take_command(bot, update):
    user_id = update.message.chat_id
    set_state(user_id=user_id, state="take")


def help_command(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text="Возможные комманды:\n"
                          "/start - Добавляет в базу данных бота id пользователя, "
                          "для последующей работы с ним\n"
                          "/add - Добавляет заказ, который вводит пользователь,"
                          "также оповещает остальных пользователей о новом заказе\n"
                          "/remove - Удаляет заказ пользователя , "
                          "также оповещает остальных пользователей, что заказ был удалён\n"
                          "/take - Использутеся для того, чтобы пользователь взял заказ по ID,"
                          "также оповещает остальных пользователей о взятом заказе \n"
                          "/help - Выводит справку о командах"
                     )


def add(bot, message, user_id):
    print("add")
    print(user_id)
    order = Order(user_id, message)
    add_order(order)
    set_state(user_id, "normal")
    user_ids = get_users_ids(filter_id=user_id)
    for rec_id in user_ids:
        bot.send_message(chat_id=rec_id,
                         text="Новый заказ был добавлен:\n" +
                              str(user_id) + "\n" + message)


def take(bot, message, user_id):
    print("take")
    print(user_id)
    # noinspection PyBroadException
    try:
        take_order(performer_id=user_id, customer_id=message)
        user_ids = get_users_ids(filter_id=user_id)
        for rec_id in user_ids:
            bot.send_message(chat_id=rec_id,
                             text="Заказ:\n" +
                                  message + "\n"
                                            "взят")
        bot.send_message(chat_id=message,
                         text="Ваш заказ был взят пользователем:\n" + str(user_id)
                         )

    except Exception:
        pass


def normal(bot, user_id):
    bot.send_message(chat_id=user_id, text="Используйте команду \n/help\n"
                                           ",чтобы получить информацию"
                                           " о возможных командах")


def update_message(bot, update):
    msg = update.message.text
    user_id = update.message.chat_id
    state = get_state(user_id)
    if state == "add":
        add(bot=bot, message=msg, user_id=user_id)
    elif state == "take":
        take(bot=bot, message=msg, user_id=user_id)
    elif state == "normal":
        normal(bot=bot, user_id=user_id)


def main():
    print_users()
    print_orders()
    token = get_token()
    updater = Updater(token)
    dispatcher = updater.dispatcher
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    msg_handler = MessageHandler(Filters.text, update_message)
    start_handler = CommandHandler('start', start_command)
    add_handler = CommandHandler('add', add_command)
    help_handler = CommandHandler('help', help_command)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(add_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(msg_handler)

    print('Connection established')
    updater.start_polling()


main()
