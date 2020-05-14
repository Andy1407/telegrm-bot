import datetime

import pytz

from formatdate import parse_date
from type import send


def reminder(bot, db):
    """
    :param telebot.TeleBot bot:
    :param database.Database db:
    :return:
    """
    while True:
        try:
            from bot import base_memory, timezone_list
            delete_list = []
            memory = db.show(table="message")
            for user in memory:  # проходит по пользователем
                id_user, date, type, message1, message2, show_message, number = user
                timezone = db.show(table="user", show_column="TIMEZONE", ID=id_user)
                now = datetime.datetime.now(tz=pytz.timezone(timezone)).replace(tzinfo=None)
                if now >= parse_date(date):
                    send(bot, int(id_user), type, message1, message2)
                    db.remove(table='message', ID=id_user, DATE=date, TYPE=type, MESSAGE1=message1, MESSAGE2=message2)
                # for index in range(len(base_memory[user]["date"])):  # проходит по датом пользователя
                #     now = datetime.datetime.now(tz=timezone_list[user])  # время сейчас
                #     for i in range(len(base_memory[user]["date"][index])):  # проходит по времени отправки сообщения
                #         deadline = base_memory[user]["date"][index][i]  # время, когда надо отправить сообщение
                #         if now.replace(tzinfo=None) >= deadline:
                #             send(bot, user, base_memory[user]["messages"][index])  # отправляет сообщение
                #             delete_list.append([user, index, i])

            # for i in delete_list:
            #
            #     base_memory[i[0]]["date"][i[1]].pop(i[2])
            #     if not base_memory[i[0]]["date"][i[1]]:
            #         base_memory[i[0]]["date"].pop(i[1])
            #         base_memory[i[0]]["messages"].pop(i[1])
            #     if not base_memory[i[0]]["messages"]:
            #         base_memory.pop(i[0])
            # with open('errors.log') as error:
            #     errors = error.read().split("\n")
            # while len(errors) > 20:
            #     errors.pop(-1)
            # with open('errors.log', "w") as error:
            #     error.write("\n".join(errors))

        except Exception:
            continue