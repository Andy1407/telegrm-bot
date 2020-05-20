from datetime import datetime

import pytz
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def create_callback_data(*data):
    """ Create the callback data associated to each button"""
    data = list(map(str, data))
    return ";".join(data)


def separate_callback_data(data):
    """ Separate the callback data"""
    return data.split(";")


def create_time(hour=None, minute=None, timezone="UTC"):
    now = datetime.now(tz=pytz.timezone(timezone)).replace(tzinfo=None)
    if hour is None:
        hour = str(now.hour)
    else:
        hour = str(hour)
    if minute is None:
        minute = str(now.minute)
    else:
        minute = str(minute)

    callback_id = "TIME"
    data_ignore = create_callback_data("IGNORE", hour, minute, callback_id)

    hour = "0" + str(hour) if len(hour) == 1 else str(hour)
    minute = "0" + str(minute) if len(minute) == 1 else str(minute)

    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("default", callback_data=create_callback_data("DEFAULT", hour, minute, callback_id)))
    row = [
        InlineKeyboardButton("⋀", callback_data=create_callback_data("NEXT_HOUR", hour, minute, callback_id)),
        InlineKeyboardButton("                ", callback_data=data_ignore),
        InlineKeyboardButton("⋀", callback_data=create_callback_data("NEXT_MINUTE", hour, minute, callback_id))]

    keyboard.row(*row)

    row = [
        InlineKeyboardButton(hour, callback_data=create_callback_data("NOW_HOUR", hour, minute, callback_id)),
        InlineKeyboardButton(":", callback_data=data_ignore),
        InlineKeyboardButton(minute, callback_data=create_callback_data("NOW_MINUTE", hour, minute, callback_id))
    ]
    keyboard.row(*row)

    row = [
        InlineKeyboardButton("⋁", callback_data=create_callback_data("LAST_HOUR", hour, minute, callback_id)),
        InlineKeyboardButton("👌", callback_data=data_ignore),
        InlineKeyboardButton("⋁", callback_data=create_callback_data("LAST_MINUTE", hour, minute, callback_id))
    ]
    keyboard.row(*row)
    keyboard.add(
        InlineKeyboardButton("cancel", callback_data=create_callback_data("CANCEL", hour, minute, callback_id)))
    return keyboard
