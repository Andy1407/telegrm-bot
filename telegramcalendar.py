#!/usr/bin/env python3
#
# A library that allows to create an inline calendar keyboard.
# grcanosa https://github.com/grcanosa
#
"""
Base methods for calendar keyboard creation and processing.
"""

import calendar
import datetime

from telebot import types

import bot as b


def create_callback_data(action, year, month, day):
    """ Create the callback data associated to each button"""
    return ";".join([action, str(year), str(month), str(day)])


def separate_callback_data(data):
    """ Separate the callback data"""
    return data.split(";")


def create_calendar(year=None, month=None):
    """
    Create an inline keyboard with the provided year and month
    :param int year: Year to use in the calendar, if None the current year is used.
    :param int month: Month to use in the calendar, if None the current month is used.
    :return: Returns the InlineKeyboardMarkup object with the calendar.
    """
    now = datetime.datetime.now()
    if year is None:
        year = now.year
    if month is None:
        month = now.month
    keyboard = types.InlineKeyboardMarkup()
    data_ignore = create_callback_data("IGNORE", year, month, 0)
    # First row - Month and Year
    row = [types.InlineKeyboardButton(calendar.month_name[month] + " " + str(year), callback_data=data_ignore)]
    keyboard.row(*row)
    # Second row - Week Days
    row = []
    for day in ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]:
        row.append(types.InlineKeyboardButton(day, callback_data=data_ignore))
    keyboard.row(*row)

    my_calendar = calendar.monthcalendar(year, month)
    for week in my_calendar:
        row = []
        for day in week:
            if day == 0:
                row.append(types.InlineKeyboardButton(" ", callback_data=data_ignore))
            else:
                row.append(
                    types.InlineKeyboardButton(str(day), callback_data=create_callback_data("DAY", year, month, day)))
        keyboard.row(*row)
    # Last row - Buttons
    keyboard.row(types.InlineKeyboardButton("<", callback_data=create_callback_data("PREV-MONTH", year, month, day)),
                 types.InlineKeyboardButton(" ", callback_data=data_ignore),
                 types.InlineKeyboardButton(">", callback_data=create_callback_data("NEXT-MONTH", year, month, day)))
    return keyboard


def process_calendar_selection(bot, message):
    """
    Process the callback_query. This method generates a new calendar if forward or
    backward is pressed. This method should be called inside a CallbackQueryHandler.
    :param telegram.Bot bot: The bot, as provided by the CallbackQueryHandler
    :param telegram.Update message: The update, as provided by the CallbackQueryHandler
    :return: Returns a tuple (Boolean,datetime.datetime), indicating if a date is selected
                and returning the date if so.
    """
    ret_data = (False, None, None)
    (action, year, month, day) = separate_callback_data(message.data)
    curr = datetime.datetime(int(year), int(month), 1)
    if action == "IGNORE":
        bot.answer_callback_query(callback_query_id=message.id)
    elif action == "DAY":
        now = datetime.datetime.now(tz=b.timezone_list[message.message.chat.id])
        now = now.replace(tzinfo=None)
        bot.edit_message_text(text=message.message.text,
                              chat_id=message.message.chat.id,
                              message_id=message.message.message_id)
        ret_data = [True, datetime.datetime(int(year), int(month), int(day)), []]
        if now < datetime.datetime(int(year), int(month), int(day), 8, 30):
            ret_data[2].append(datetime.datetime(int(year), int(month), int(day), 8, 30))
        if now < datetime.datetime(int(year), int(month), int(day), 12):
            ret_data[2].append(datetime.datetime(int(year), int(month), int(day), 12))
        if now < datetime.datetime(int(year), int(month), int(day), 15, 30):
            ret_data[2].append(datetime.datetime(int(year), int(month), int(day), 15, 30))
        if now < datetime.datetime(int(year), int(month), int(day), 20):
            ret_data[2].append(datetime.datetime(int(year), int(month), int(day), 20))
        else:
            bot.send_message(message.message.chat.id, "I cannot set this date.")
            ret_data[0] = False
    elif action == "PREV-MONTH":
        pre = curr - datetime.timedelta(days=1)
        bot.edit_message_text(text=message.message.text,
                              chat_id=message.message.chat.id,
                              message_id=message.message.message_id,
                              reply_markup=create_calendar(int(pre.year), int(pre.month)))
    elif action == "NEXT-MONTH":
        ne = curr + datetime.timedelta(days=calendar.monthrange(curr.year, curr.month)[1])
        bot.edit_message_text(text=message.message.text,
                              chat_id=message.message.chat.id,
                              message_id=message.message.message_id,
                              reply_markup=create_calendar(int(ne.year), int(ne.month)))
    else:
        bot.answer_callback_query(callback_query_id=message.id, text="Something went wrong!")
        # UNKNOWN
    return ret_data
