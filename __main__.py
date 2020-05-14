from threading import Thread

import telebot as tb

import reminder
from bot import bot
from database import Database


def main():
    TOKEN = "731585587:AAFoo1xgnU7wBo92Yjwt1t-AKZFadpLFKRs"

    db = Database(name_database="db")
    db.add_tables(name_table="message", ID="INT", DATE="TEXT", TYPE="TEXT", MESSAGE1="TEXT", MESSAGE2="TEXT",
                  SHOW_MESSAGE="TEXT", NUMBER="INT")
    db.add_tables(name_table="user", ID="INT", TIMEZONE="TEXT")

    base_bot = tb.TeleBot(TOKEN)

    tread_bot = Thread(target=bot, args=(base_bot, db,))
    tread_reminder = Thread(target=reminder.reminder, args=(base_bot, db,))

    tread_bot.start()
    tread_reminder.start()

    tread_bot.join()
    tread_reminder.join()


if __name__ == '__main__':
    main()
