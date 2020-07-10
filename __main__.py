import os
from threading import Thread

import telebot as tb

import reminder
from bot import botHandler
from database import Database


def main():
    TOKEN = os.environ.get('TOKEN') or ''

    bot = tb.TeleBot(TOKEN)

    db = Database()

    tread_bot = Thread(target=botHandler, args=(bot, db), daemon=True)
    tread_reminder = Thread(target=reminder.reminder, args=(bot, db), daemon=True)

    tread_bot.start()
    tread_reminder.start()

    tread_bot.join()
    tread_reminder.join()


if __name__ == '__main__':
    main()
