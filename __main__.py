import os
from threading import Thread

import telebot as tb

import reminder
from bot import bot
from database import Database


def main():
    TOKEN = os.environ.get('TOKEN') or ''

    base_bot = tb.TeleBot(TOKEN)

    db = Database()
    tread_bot = Thread(target=bot, args=(base_bot, db), daemon=True)
    tread_reminder = Thread(target=reminder.reminder, args=(base_bot, db), daemon=True)

    tread_bot.start()
    tread_reminder.start()

    tread_bot.join()
    tread_reminder.join()


if __name__ == '__main__':
    main()
