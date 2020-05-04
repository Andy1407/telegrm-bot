import datetime

import pytz

from type import send


def reminder(bot):
    while True:
        from bot import base_memory, timezone_list
        delete_list = []
        for user in base_memory:

            for index in range(len(base_memory[user]["date"])):
                now = datetime.datetime.now(tz=pytz.timezone(timezone_list[user]))
                for i in range(len(base_memory[user]["date"][index])):
                    deadline = base_memory[user]["date"][index][i].astimezone(pytz.timezone(timezone_list[user]))
                    if now.replace(tzinfo=None) >= deadline.replace(tzinfo=None):
                        send(bot, user, base_memory[user]["messages"][index])
                        delete_list.append([user, index, i])
        for i in delete_list:

            base_memory[i[0]]["date"][i[1]].pop(i[2])
            if not base_memory[i[0]]["date"]:
                base_memory[i[0]]["date"].pop(i[1])
                base_memory[i[0]]["messages"].pop(i[1])
            if not base_memory[i[0]]["messages"]:
                base_memory.pop(i[0])
