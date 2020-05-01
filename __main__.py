import telebot as tb
from threading import Thread
from bot import bot
import reminder


def main():
    TOKEN = "731585587:AAFoo1xgnU7wBo92Yjwt1t-AKZFadpLFKRs"

    base_bot = tb.TeleBot(TOKEN)

    tread_bot = Thread(target=bot, args=(base_bot,))
    tread_reminder = Thread(target=reminder.reminder, args=(base_bot,))

    tread_bot.start()
    tread_reminder.start()

    tread_bot.join()
    tread_reminder.join()


if __name__ == '__main__':
    main()
