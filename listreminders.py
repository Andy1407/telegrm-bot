from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from formatdate import parse_date


def create_list(message):
    list_reminders = InlineKeyboardMarkup()
    for i in range(len(message)):
        user_id, date, type, message1, message2, show_message, number = message[i]
        list_reminders.add(
            InlineKeyboardButton(f"{type}: {show_message}" + f" {parse_date(date).strftime('%d.%m.%Y')}",
                                 callback_data=f"{show_message};{parse_date(date).strftime('%d.%m.%Y')};{number};1"))
    list_reminders.add(InlineKeyboardButton("cancel", callback_data=f"CANCEL;;;1"))

    return list_reminders


def option(number, reminder):
    list_reminders = InlineKeyboardMarkup()
    list_reminders.add(InlineKeyboardButton("edit", callback_data=f"EDIT;{number};{reminder};2"))
    list_reminders.add(InlineKeyboardButton("delete", callback_data=f"DELETE;{number};{reminder};2"))
    list_reminders.add(InlineKeyboardButton("cancel", callback_data=f"CANCEL;{number};{reminder};2"))
    return list_reminders


def edit(number):
    edit_list = InlineKeyboardMarkup()
    edit_list.add(InlineKeyboardButton("edit the text", callback_data=f"EDIT_TEXT;{number};3"))
    edit_list.add(InlineKeyboardButton("edit the date", callback_data=f"EDIT_DATE;{number};3"))
    edit_list.add(InlineKeyboardButton("cancel", callback_data=f"CANCEL;{number};3"))
    return edit_list


def process_reminder_selection(bot, message):
    if message.data.split(";")[0] == "CANCEL":
        bot.delete_message(chat_id=message.message.chat.id, message_id=message.message.message_id)
    else:
        bot.edit_message_text(text=message.data.split(";")[0]+f"({message.data.split(';')})",
                              chat_id=message.message.chat.id,
                              message_id=message.message.message_id,
                              reply_markup=option(message.data.split(";")[2], message.data.split(";")[0]))


def process_option_selection(bot, message):
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
