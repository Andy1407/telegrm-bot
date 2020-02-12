import datetime


def reminder(message, bot, text, date, time):
    with open("memory") as m:
        memory = m.readline().split(";")

    while True:
        for i in memory:
            deadline = datetime.datetime(int(memory[3][2]), int(memory[3][1]), int(memory[3][0]), int(memory[4][0])-3, int(memory[4][1]), int(memory[4][2]))
            bot.send_message(message.from_user.id, "Wait for a reminder.")
            now = datetime.datetime.now()
            if now >= deadline:
                memory[1].send_message(memory[0].from_user.id, text)
                break
