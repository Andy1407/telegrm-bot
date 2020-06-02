from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from add.formatdate import parse_date


def create_list(message):
    """
    create of reminder list
    :param list message: list of reminder
    :return: Returns the InlineKeyboardMarkup object with the reminder list.
    """
    list_reminders = InlineKeyboardMarkup()
    number_list = []
    for i in range(len(message)):
        user_id, date, type, message1, message2, show_message, number = message[i]
        if number not in number_list:
            list_reminders.add(
                InlineKeyboardButton(f"{show_message}" + f" ({parse_date(date).strftime('%d.%m.%Y')})",
                                     callback_data=f"{show_message};{parse_date(date).strftime('%d.%m.%Y')};{number};1"))

        number_list.append(number)
    list_reminders.add(InlineKeyboardButton("cancel", callback_data=f"CANCEL;;;1"))

    return list_reminders


def option(number, reminder):
    """
    create of menu for edit or delete reminder
    :param str number: number of reminder
    :param str reminder: reminder, which you chose
    :return: Returns the InlineKeyboardMarkup object with the list of options.
    """
    list_reminders = InlineKeyboardMarkup()
    list_reminders.add(InlineKeyboardButton("edit", callback_data=f"EDIT;{number};{reminder};2"))
    list_reminders.add(InlineKeyboardButton("delete", callback_data=f"DELETE;{number};{reminder};2"))
    list_reminders.add(InlineKeyboardButton("cancel", callback_data=f"CANCEL;{number};{reminder};2"))
    return list_reminders


def edit(number):
    """
    create of detailed menu for edit reminder
    :param str number: number of reminder
    :return: Returns the InlineKeyboardMarkup object with the edit list.
    """
    edit_list = InlineKeyboardMarkup()
    edit_list.add(InlineKeyboardButton("edit the text", callback_data=f"EDIT_TEXT;{number};3"))
    edit_list.add(InlineKeyboardButton("edit the date", callback_data=f"EDIT_DATE;{number};3"))
    edit_list.add(InlineKeyboardButton("cancel", callback_data=f"CANCEL;{number};3"))
    return edit_list


def processing_selected_reminder(bot, message):
    """processing the selected reminder"""
    show_message, date, number, step = message.data.split(";")
    if show_message == "CANCEL":
        bot.delete_message(chat_id=message.message.chat.id, message_id=message.message.message_id)
    else:
        bot.edit_message_text(text=show_message + f"({date}):",
                              chat_id=message.message.chat.id,
                              message_id=message.message.message_id,
                              reply_markup=option(number, show_message))


def processing_selected_option(bot, message):
    """processing the selected option"""
    action, number, reminder, step = message.data.split(";")
    if action == "CANCEL":
        bot.delete_message(chat_id=message.message.chat.id, message_id=message.message.message_id)
    elif action == "EDIT":
        bot.edit_message_text(text=f"edit the message({reminder}):",
                              chat_id=message.message.chat.id,
                              message_id=message.message.message_id,
                              reply_markup=edit(number))
    else:
        bot.answer_callback_query(callback_query_id=message.id, text="Something went wrong!")
