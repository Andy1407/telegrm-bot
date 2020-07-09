import datetime

import pytz

from add.formatdate import parse_date
from add.type import send


def reminder(bot, db):
    """
    views of database and show reminder in due time
    :param telebot.TeleBot bot: bot
    :return: nothing
    """

    while True:
        try:
            db.connect()
            memory = db.select(table="messages")
            for user in memory:
                id_user, date, type, message1, message2, show_message, number = user
                timezone = db.select(table="users", column="timezone", id=id_user)[0][0]
                now = datetime.datetime.now(tz=pytz.timezone(timezone)).replace(tzinfo=None)
                if now >= parse_date(date):
                    send(bot, int(id_user), type, message1, message2)
                    db.remove(table='messages', user_id=id_user, date=f"'{date}'", id=number)

        except Exception:
            continue
