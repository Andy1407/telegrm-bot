import datetime
from type import send


def reminder(bot):
    while True:
        from bot import base_memory
        delete_list = []
        for user in base_memory:
            for index in range(len(base_memory[user]["date"])):
                now = datetime.datetime.now()
                deadline = base_memory[user]["date"][index]
                if now >= deadline:
                    send(bot, user, base_memory[user]["messages"][index])
                    # bot.send_message(user, base_memory[user]["message"][index])
                    delete_list.append([user, index])
        for i in delete_list:
            base_memory[i[0]]["messages"].pop(i[1])
            base_memory[i[0]]["date"].pop(i[1])
            if not base_memory[i[0]]["messages"]:
                base_memory.pop(i[0])
