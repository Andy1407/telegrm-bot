import datetime


def reminder(message, bot, text, date, time):

    deadline = datetime.datetime(int(date[2]), int(date[1]), int(date[0]), int(time[0])-3, int(time[1]), int(time[2]))
    bot.send_message(message.from_user.id, "Wait for a reminder.")

    while True:

        now = datetime.datetime.now()
        if now >= deadline:
            bot.send_message(message.from_user.id, text)
            break
