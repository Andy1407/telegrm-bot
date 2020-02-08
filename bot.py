import telebot as tb
import datetime

from reminder import reminder


TOKEN = "731585587:AAFoo1xgnU7wBo92Yjwt1t-AKZFadpLFKRs"

bot = tb.TeleBot(TOKEN)


text = " "
number = 0
now = datetime.datetime.now()
date=[now.day, now.month, now.year]
time = [12, 19, 13]
error = False


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.from_user.id, "Enter the text you want to remember.")


@bot.message_handler(commands=['cancel'])
def cancel_message(message):
    global number
    bot.send_message(message.from_user.id, "The reminder is cancelled.")
    number = 0


@bot.message_handler(commands=['reminder'])
def reminder_message(message):
    if len(date) >= 3 and len(time) >= 3 and not(error):
        reminder(message, bot, text, date, time)
    else:
        bot.send_message(message.from_user.id, "You didn't enter any data.")


@bot.message_handler(content_types=["text"])
def text_messages(message):
    global text
    global date
    global time
    global number
    global error

    if number == 0:
        text = message.text
        number = 1
        bot.send_message(message.from_user.id, "Entered date.")
    elif number == 1:
        try:
            date = message.text.split(".")
            if len(date) < 3:
                date.append("error")
            date = map(int, date)
            bot.send_message(message.from_user.id, "Enter the time(if the time is not important, enter a space).")
        except ValueError:
            bot.send_message(message.from_user.id, "You entered the wrong format, try again.")
            error = True
        else:
            number = 2

    elif number == 2:
        try:
            if message.text != " ":
                time = message.text.split(":")
            if len(time) < 2:
                time.append("error")
            elif len(time) == 2:
                time.append(0)
            date = map(int, date)
            bot.send_message(message.from_user.id, "Enter '/reminder' to set a reminder.")
        except ValueError:
            bot.send_message(message.from_user.id, "You entered the wrong format, try again.")
            error = True
        else:
            number = 0


bot.polling(none_stop=True, interval=0)