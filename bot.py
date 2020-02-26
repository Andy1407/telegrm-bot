import telebot as tb
import datetime
import os

TOKEN = "731585587:AAFoo1xgnU7wBo92Yjwt1t-AKZFadpLFKRs"

bot = tb.TeleBot(TOKEN)

text = " "
number = 0
now = datetime.datetime.now()
date = [now.day + 1, now.month, now.year]
time = [now.hour, now.minute + 1, now.second]
error = False
local_memory = {}


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.from_user.id, "Enter the text you want to remember.")


@bot.message_handler(commands=['cancel'])
def cancel_message(message):
    global number
    bot.send_message(message.from_user.id, "The reminder is cancelled.")
    with open("memory.txt", "w") as m:
        m.write("")
    number = 0


@bot.message_handler(commands=['reminder'])
def reminder_message(message):
    if len(date) >= 3 and (len(time) >= 3 or time[0].lower() == "no") and not (error):

        with open('memory.txt', 'r+') as m:
            old_memory = m.read()
            m.write(old_memory + str(message.from_user.id) + ":" + text + ":" + str(date[2]) + ":" + str(
                date[1]) + ":" + str(date[0]) + ":" + str(time[0]) + ":" + str(time[1]) + ":" + str(time[2]) + ";")

        bot.send_message(message.from_user.id, "wait for a reminder.")
    else:
        bot.send_message(message.from_user.id, "You didn't enter any data.")


@bot.message_handler(content_types=["text"])
def text_messages(message):
    global text
    global date
    global time
    global number
    global error
    global now
    if message.from_user.id not in local_memory:
        local_memory[message.from_user.id] = {"number": number, "text": text, "date": date, "time": time, "error": error}

    if local_memory[message.from_user.id]["number"] == 0:
        local_memory[message.from_user.id]["text"] = message.text
        local_memory[message.from_user.id]["number"] = 1
        bot.send_message(message.from_user.id, "Entered date (xx.xx.xxxx). if the time is not important, enter a 'no'")  # after the text
    elif local_memory[message.from_user.id]["number"] == 1:
        try:
            if message.text.lower() != "no":
                local_memory[message.from_user.id]["date"] = message.text.split(".")

            if len(local_memory[message.from_user.id]["date"]) < 3:
                local_memory[message.from_user.id]["date"].append("error")
            local_memory[message.from_user.id]["date"] = list(map(int, local_memory[message.from_user.id]["time"]))
            bot.send_message(message.from_user.id,
                             "Enter the time(if the time is not important, enter a 'no').")  # after the date
        except ValueError:
            bot.send_message(message.from_user.id, "You entered the wrong format, try again.")
            error = True
            local_memory[message.from_user.id]["error"] = True
        else:
            local_memory[message.from_user.id]["number"] = 2
            local_memory[message.from_user.id]["error"]

    elif local_memory[message.from_user.id]["number"] == 2:
        try:
            if message.text != " ":
                local_memory[message.from_user.id]["time"] = message.text.split(":")

            if len(local_memory[message.from_user.id]["time"]) < 2 and local_memory[message.from_user.id]["time"][0].lower() != 'no':
                local_memory[message.from_user.id]["time"].append("error")
            elif len(local_memory[message.from_user.id]["time"]) == 2 and local_memory[message.from_user.id]["time"][0].lower() != 'no':
                local_memory[message.from_user.id]["time"].append(0)
            if local_memory[message.from_user.id]["time"][0].lower() != 'no':
                local_memory[message.from_user.id]["time"] = list(map(int, local_memory[message.from_user.id]["time"]))
            else:
                local_memory[message.from_user.id]["time"] = [now.hour, now.minute + 1, now.second]
            bot.send_message(message.from_user.id, "Enter '/reminder' to set a reminder.")
        except ValueError:
            bot.send_message(message.from_user.id, "You entered the wrong format, try again.")
            local_memory[message.from_user.id]["error"] = True
        else:
            local_memory[message.from_user.id]["number"] = 0
            local_memory[message.from_user.id]["error"] = False


bot.polling(none_stop=True, interval=0)
