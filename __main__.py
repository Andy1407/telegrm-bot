import os
from threading import Thread

import telebot as tb

import reminder
from bot import botHandler
from database import Database

from pyrogram import Client, filters
from pyrogram.errors import FloodWait

from time import sleep

def userBot():
    app = Client("my_account")


    @app.on_message(filters.me)
    def type(_, msg):
        orig_text = msg.text
        text = orig_text[1:]
        percent = int(len(orig_text) / 100)
        tbp = ""
        typing_symbol = "|"

        for i in orig_text:
            try:
                tbp = f"{tbp}{i}"
                msg.edit(f"{percent}% " + tbp + typing_symbol)
                percent = int(len(tbp)/(len(orig_text) / 100))
                sleep(0.1)

            except FloodWait as e:
                sleep(e.x)

        try:
            msg.edit(orig_text)
        except FloodWait as e:
            sleep(e.x)


    app.run()


def main():
#     TOKEN = os.environ.get('TOKEN') or ''

#     bot = tb.TeleBot(TOKEN)

#     db = Database()

#     tread_bot = Thread(target=botHandler, args=(bot, db), daemon=True)
#     tread_reminder = Thread(target=reminder.reminder, args=(bot, db), daemon=True)
    thread_userBot = Thread(target=userBot, daemon=True)

    # tread_bot.start()
    # tread_reminder.start()
    thread_userBot.start()

    # tread_bot.join()
    # tread_reminder.join()
    thread_userBot.join()


if __name__ == '__main__':
    main()
