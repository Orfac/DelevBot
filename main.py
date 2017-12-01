import logging

from telegram.ext import CommandHandler
from telegram.ext import Updater

from pymongo import MongoClient
#dfsdf
from order import *
from bot_token import *
from user import *


def start_command(bot, update):
    current_chat_id = update.message.chat_id
    bot.send_message(chat_id=current_chat_id,
                     text="Вас приветствует EasyDelev бот!"
                          "Создавайте заказы, которые вы хотите,"
                          "чтобы другие пользователи купили вам."
                          " Также не забывайте сами брать заказы других пользователей."
                          "Удачи!"
                     )
    print(current_chat_id)
    add_new_user(current_chat_id)


def add_command(bot, update):
    users = get_users()
    print(update.message)
    current_chat_id = update.message.chat_id
    bot.send_message(chat_id=update.message.chat_id, text="Введите необходимые данные о заказе\n")


def remove_command(bot, update):
    pass


def take_command(bot, update):
    pass


def help_command(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text="Возможные комманды:\n"
                          "/start - Добавляет в базу данных бота id пользователя, "
                          "для последующей работы с ним\n"
                          "/add - Добавляет заказ, который вводит пользователь,"
                          "также оповещает остальных пользователей о новом заказе\n"
                          "/remove - Удаляет заказ, по ID , "
                          "который пользователь вводит следующим сообщением\n"
                          "/take - Использутеся для того, чтобы пользователь взял заказ по ID,"
                          "также оповещает остальных пользователей о взятом заказе \n"
                          "/leave - Используется для выхода из группы пользователей этого бота\n"
                          "/help - Выводит справку о командах"
                     )


def main():
    client = MongoClient()
    db = client['BotDB']
    users = db['Users']
    users.drop()
    orders = db['Orders']
    orders.drop()

    print_all_users()
    token = get_token()
    updater = Updater(token)
    dispatcher = updater.dispatcher
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    start_handler = CommandHandler('start', start_command)
    add_handler = CommandHandler('add', add_command)
    help_handler = CommandHandler('help', help_command)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(add_handler)
    dispatcher.add_handler(help_handler)

    print('Connection established')
    updater.start_polling()


main()
