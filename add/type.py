def send(bot, chat, type, message1, message2):
    """
    send reminder
    :param str message2: message
    :param str message1: message
    :param str type: type
    :param int chat: chat id
    :param telebot.TeleBot bot: bot
    :return: nothing
    """
    if type == "text":
        bot.send_message(chat, message1)

    elif type == "audio":
        bot.send_audio(chat, message1)

    elif type == "document":
        bot.send_document(chat, message1)

    elif type == "photo":
        bot.send_photo(chat, message1)

    elif type == "sticker":
        bot.send_sticker(chat, message1)

    elif type == "video":
        bot.send_video(chat, message1)

    elif type == "video_note":
        bot.send_video_note(chat, message1)

    elif type == "voice":
        bot.send_voice(chat, message1)

    elif type == "location":
        bot.send_location(chat, float(message1), float(message2))

    elif type == "contact":
        bot.send_contact(chat, message1, message2)


def record(message):
    """
    returns data for record in database
    :param telebot.types.Message message:
    :return: returns data for record in database
    """
    if message.content_type == "text":
        return str(message.text), "NULL"

    elif message.content_type == "audio":
        return str(message.audio.file_id), "NULL"

    elif message.content_type == "document":
        return str(message.document.file_id), "NULL"

    elif message.content_type == "photo":
        return str(message.photo[0].file_id), "NULL"

    elif message.content_type == "sticker":
        return str(message.sticker.file_id), "NULL"

    elif message.content_type == "video":
        return str(message.video.file_id), "NULL"

    elif message.content_type == "video_note":
        return str(message.video_note.file_id), "NULL"

    elif message.content_type == "voice":
        return str(message.voice.file_id), "NULL"

    elif message.content_type == "location":
        return str(message.location.latitude), str(message.location.longitude)

    elif message.content_type == "contact":
        return str(message.contact.phone_number), str(message.contact.first_name)


def view_name(message):
    """
    returns data for show in list of reminder
    :param telebot.types.Message message: message, which should be shown
    :return: returns data for show in list of reminder
    """
    if message.content_type == "text":
        return f"{message.content_type}: {message.text}"
    elif message.content_type == "audio":
        return f"{message.content_type}: {message.audio.title}"
    elif message.content_type == "document":
        return f"{message.content_type}: {message.document.file_name}"
    elif message.content_type == "photo":
        return f"{message.content_type}: {message.photo.file_size}"
    elif message.content_type == "sticker":
        return f"{message.content_type}: {message.sticker.emoji}"
    elif message.content_type == "video":
        return f"{message.content_type}: {message.video.duration} seconds"
    elif message.content_type == "video_note":
        return f"{message.content_type}: {message.video_note.duration} seconds"
    elif message.content_type == "voice":
        return f"{message.content_type}: {message.voice.duration}"
    elif message.content_type == "location":
        return f"{message.content_type}: {message.location.address}"
    elif message.content_type == "contact":
        return f"{message.content_type}: {message.contact.phone_number}"


def number_of_reminder(message):
    """returns next number for reminder"""
    maximum = 0
    for i in message:
        if int(i[0]) > maximum:
            maximum = int(i[0])

    minimum = maximum
    for i in message:
        if int(i[0]) < minimum:
            minimum = int(i[0])
    if minimum <= 1:
        return maximum + 1
    else:
        return minimum - 1