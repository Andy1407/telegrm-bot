import telebot as tb
import datetime
import os

TOKEN = "731585587:AAFoo1xgnU7wBo92Yjwt1t-AKZFadpLFKRs"

bot = tb.TeleBot(TOKEN)

text = " "
number = 0
now = datetime.datetime.now()
date = [now.day + 1, now.month, now.year]
time = [now.hour, now.minute + 4, now.second]
error = False
local_memory = {}


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.from_user.id, "Enter the text you want to remember.")


@bot.message_handler(commands=['cancel'])
def cancel_message(message):
    global local_memory
    
    bot.send_message(message.from_user.id, "The reminder is cancelled.")
    with open("memory.txt", "w") as m:
        m.write("")
    if message.from_user.id in local_memory:
        local_memory.pop(message.from_user.id)
# /back


@bot.message_handler(commands=['back'])
def start_message(message):
    global local_memory
    
    if local_memory[message.from_user.id][number] == 0:
        bot.send_message(message.from_user.id, "you cannot go back to the previous step")
        
    if local_memory[message.from_user.id][number] > 0:
        local_memory[message.from_user.id][number] -= 1
        
    if local_memory[message.from_user.id][number] == 1:
        bot.send_message(message.from_user.id, "Entered date (xx.xx.xxxx). If the date is not important, enter a 'no'")
    elif local_memory[message.from_user.id][number] == 2:
        bot.send_message(message.from_user.id, "Enter the time. If the time is not important, enter a 'no'.")
    elif local_memory[message.from_user.id][number] == 3:
        bot.send_message(message.from_user.id, "Enter '/reminder' to set a reminder.")
    
    bot.send_message(message.from_user.id, "repeat the action")

# /reminder  
@bot.message_handler(commands=['reminder'])
def reminder_message(message):
    global local_memory
    
    if message.from_user.id not in local_memory:
        local_memory[message.from_user.id] = {"number": number, "text": text, "date": date, "time": time, "error": error}
    
    
    if not (local_memory[message.from_user.id]["error"]) and local_memory[message.from_user.id]["number"] == 3:

        with open('memory.txt', 'r+') as m:
            old_memory = m.read()
            
            m.write(old_memory + str(message.from_user.id) + ":" + local_memory[message.from_user.id]["text"] +
                    ":" + str(local_memory[message.from_user.id]["date"][2]) + 
                    ":" + str(local_memory[message.from_user.id]["date"][1]) + 
                    ":" + str(local_memory[message.from_user.id]["date"][0]) + 
                    ":" + str(local_memory[message.from_user.id]["time"][0]) + 
                    ":" + str(local_memory[message.from_user.id]["time"][1]) + 
                    ":" + str(local_memory[message.from_user.id]["time"][2]) + ";")
            
        bot.send_message(message.from_user.id, "wait for a reminder.")
              

        local_memory.pop(message.from_user.id)
        
        local_memory[message.from_user.id]["number"] == 0


    else:
        bot.send_message(message.from_user.id, "You didn't enter any data.")


@bot.message_handler(content_types=["text"])
def text_messages(message):
    global local_memory

    if message.from_user.id not in local_memory:
        local_memory[message.from_user.id] = {"number": number, "text": text, "date": date, "time": time, "error": error}

    if local_memory[message.from_user.id]["number"] == 0:
        local_memory[message.from_user.id]["text"] = message.text
        local_memory[message.from_user.id]["number"] = 1
        bot.send_message(message.from_user.id, "Entered date (xx.xx.xxxx). If the date is not important, enter a 'no'")  # after the text
    elif local_memory[message.from_user.id]["number"] == 1:
        try:
            local_memory[message.from_user.id]["date"] = message.text.split(".")
            if message.text.lower() != "no":
                local_memory[message.from_user.id]["date"] = list(map(int, local_memory[message.from_user.id]["date"]))
            else:
                local_memory[message.from_user.id]["date"] = [now.day + 1, now.month, now.year]
                

            if len(local_memory[message.from_user.id]["date"]) < 3:
                local_memory[message.from_user.id]["date"].append("error")
            
            if local_memory[message.from_user.id]["date"][1] in range(1, 13) and local_memory[message.from_user.id]["date"][0] in range(1, 32):
                bot.send_message(message.from_user.id, "Enter the time. If the time is not important, enter a 'no'.")  # after the date
            else:
                local_memory[message.from_user.id]["date"].append("error")
                
               
        except ValueError:
            
            bot.send_message(message.from_user.id, "You entered the wrong format, try again.")
            local_memory[message.from_user.id]["error"] = True
        else:
            local_memory[message.from_user.id]["number"] = 2
            local_memory[message.from_user.id]["error"] = False

    elif local_memory[message.from_user.id]["number"] == 2:
        try:
            local_memory[message.from_user.id]["time"] = message.text.split(":")

            if len(local_memory[message.from_user.id]["time"]) < 2 and local_memory[message.from_user.id]["time"][0].lower() != 'no':
                local_memory[message.from_user.id]["time"].append("error")
            elif len(local_memory[message.from_user.id]["time"]) == 2 and local_memory[message.from_user.id]["time"][0].lower() != 'no':
                local_memory[message.from_user.id]["time"].append(0)
            if local_memory[message.from_user.id]["time"][0].lower() != 'no':
                local_memory[message.from_user.id]["time"] = list(map(int, local_memory[message.from_user.id]["time"]))
            else:
                local_memory[message.from_user.id]["time"] = [now.hour, now.minute + 4, now.second]
            if local_memory[message.from_user.id]["time"][0] < 24 and local_memory[message.from_user.id]["time"][1] < 60 and local_memory[message.from_user.id]["time"][2] < 60:
                bot.send_message(message.from_user.id, "Enter '/reminder' to set a reminder.")
            else:
                local_memory[message.from_user.id]["time"].append("error")
        except ValueError:
            bot.send_message(message.from_user.id, "You entered the wrong format, try again.")
            local_memory[message.from_user.id]["error"] = True
        else:
            local_memory[message.from_user.id]["number"] = 3
            local_memory[message.from_user.id]["error"] = False


bot.polling(none_stop=True, interval=0)
