from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def text_list(message):
    if message.content_type == "text":
        return f"{message.content_type}: {message.text}"
    elif message.content_type == "audio":
        return f"{message.content_type}: {message.audio.title}"
    elif message.content_type == "document":
        return f"{message.content_type}: {message.document.file_name}"
    elif message.content_type == "photo":
        return f"{message.content_type}: {message.photo.file_size}"
    elif message.content_type == "sticker":
        return f"{message.content_type}: {message.sticker.set_name}"
    elif message.content_type == "video":
        return f"{message.content_type}: {message.video.duration}"
    elif message.content_type == "video_note":
        return f"{message.content_type}: {message.video_note.duration}"
    elif message.content_type == "voice":
        return f"{message.content_type}: {message.voice.duration}"
    elif message.content_type == "location":
        return f"{message.content_type}: {message.location.address}"
    elif message.content_type == "contact":
        return f"{message.content_type}: {message.contact.phone_number}"


def create_list(messages, date):
    list_reminders = InlineKeyboardMarkup()
    for i in range(len(messages)):
        list_reminders.add(
            InlineKeyboardButton(text_list(messages[i]) + f" {date[i][0].strftime('%d.%m.%Y')}",
                                 callback_data=f"{text_list(messages[i])} {date[i][0].strftime('%d.%m.%Y')};{i};list"))
    list_reminders.add(InlineKeyboardButton("cancel", callback_data=f"CANCEL;;list"))

    return list_reminders


def option(i):
    list_reminders = InlineKeyboardMarkup()
    list_reminders.add(InlineKeyboardButton("edit", callback_data=f"EDIT;{i}"))
    list_reminders.add(InlineKeyboardButton("delete", callback_data=f"DELETE;{i}"))
    list_reminders.add(InlineKeyboardButton("cancel", callback_data="CANCEL"))
    return list_reminders


def edit(index, reminder):
    edit_list = InlineKeyboardMarkup()
    edit_list.add(InlineKeyboardButton("edit the text", callback_data=f"EDIT_TEXT;{index};{reminder}"))
    edit_list.add(InlineKeyboardButton("edit the date", callback_data=f"EDIT_DATE;{index};{reminder}"))
    edit_list.add(InlineKeyboardButton("cancel", callback_data=f"CANCEL;{index};{reminder}"))
    return edit_list


def process_reminder_selection(bot, message):
    if message.data.split(";")[0] == "CANCEL":
        bot.delete_message(chat_id=message.message.chat.id, message_id=message.message.message_id)
    else:
        bot.edit_message_text(text=message.data.split(";")[0],
                              chat_id=message.message.chat.id,
                              message_id=message.message.message_id,
                              reply_markup=option(message.data.split(";")[1], message.data.split(";")[0]))


def process_option_selection(bot, message):
    action, index, reminder = message.data.split(";")
    if action == "CANCEL":
        bot.delete_message(chat_id=message.message.chat.id, message_id=message.message.message_id)
    elif action == "EDIT":
        bot.edit_message_text(text=f"edit the message({reminder}):",
                              chat_id=message.message.chat.id,
                              message_id=message.message.message_id,
                              reply_markup=edit(index))
    else:
        bot.answer_callback_query(callback_query_id=message.id, text="Something went wrong!")
