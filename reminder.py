import datetime

import pytz

from add.database import Database
from add.formatdate import parse_date
from add.type import send


def reminder(bot):
    """
    :param telebot.TeleBot bot:
    :return: return reminder in due time
    """

    while True:
        try:
            db = Database('db')
            memory = db.show(table="message")
            for user in memory:
                id_user, date, type, message1, message2, show_message, number = user
                timezone = db.show(table="user", show_column="TIMEZONE", ID=id_user)[0][0]
                print(timezone)
                now = datetime.datetime.now(tz=pytz.timezone(timezone)).replace(tzinfo=None)
                if now >= parse_date(date):
                    send(bot, int(id_user), type, message1, message2)
                    db.remove(table='message', ID=id_user, DATE=date, NUMBER=number)

        except Exception:
            continue