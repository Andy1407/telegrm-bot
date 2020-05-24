from threading import Thread

import telebot as tb

import reminder
from add.database import Database
from bot import bot


def main():
    TOKEN = "731585587:AAFoo1xgnU7wBo92Yjwt1t-AKZFadpLFKRs"

    base_bot = tb.TeleBot(TOKEN)

    db = Database('db')
    db.add_table(name_table="message", ID="INT", DATE="TEXT", TYPE="TEXT", MESSAGE1="TEXT", MESSAGE2="TEXT",
                 SHOW_MESSAGE="TEXT", NUMBER="INT")
    db.add_table(name_table="user", ID="INT", TIMEZONE="TEXT")
    # @base_bot.message_handler(commands="reminder")
    # def reminder(message):
    #     base_bot.send_message(message.chat.id, "hello:", reply_markup=create_time())
    # base_bot.polling()

    tread_bot = Thread(target=bot, args=(base_bot,), daemon=True)
    tread_reminder = Thread(target=reminder.reminder, args=(base_bot,), daemon=True)

    tread_bot.start()
    tread_reminder.start()

    tread_bot.join()
    tread_reminder.join()


if __name__ == '__main__':
    main()
