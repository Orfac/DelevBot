import logging

from telegram.ext import CommandHandler
from telegram.ext import Updater

from pymongo import MongoClient

from order import *
from bot_token import *
from user import *

def start(bot, update):
    current_chat_id = update.message.chat_id
    bot.send_message(chat_id=current_chat_id, text="I'm a bot, please talk to me!")
    print(current_chat_id)
    add_new_user(current_chat_id)

def add(bot, update):
    users = get_users()
    print(update.message)
    current_chat_id = update.message.chat_id
    bot.send_message(chat_id=update.message.chat_id, text="It's a common message for everybody")



def main():

    print_all_users()
    token = get_token()
    updater = Updater(token)
    dispatcher = updater.dispatcher
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    start_handler = CommandHandler('start', start)
    send_msgs_handler = CommandHandler('add', add)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(send_msgs_handler)
    print('Connection established')
    updater.start_polling()


main()
