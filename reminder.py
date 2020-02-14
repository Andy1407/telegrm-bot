import datetime
import telebot as tb

TOKEN = "731585587:AAFoo1xgnU7wBo92Yjwt1t-AKZFadpLFKRs"

bot = tb.TeleBot(TOKEN)

while True:
    with open('memory.txt') as m:
        memory = m.read().split(";")  
    for i in memory:
        memory1 = i.split(":")
        if len(memory1) >= 8:
            now = datetime.datetime.now()

            deadline = datetime.datetime(int(memory1[2]), int(memory1[3]), int(memory1[4]), int(memory1[5])-3, int(memory1[6]), int(memory1[7]))

            if now >= deadline:
                bot.send_message(memory1[0], memory1[1])

                with open('memory.txt', 'r+') as m:
                    memory_all = m.read()
                    memory_all.pop(memory.index(i))
                    m.write(memory_all)
