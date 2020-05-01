def send(bot, chat, message):
    if message.content_type == "text":
        bot.send_message(chat, message.text)
    elif message.content_type == "audio":
        bot.send_audio(chat, message.audio.file_id)
    elif message.content_type == "document":
        bot.send_document(chat, message.document.file_id)
    elif message.content_type == "photo":
        bot.send_photo(chat, message.photo[0].file_id)
    elif message.content_type == "sticker":
        bot.send_sticker(chat, message.sticker.file_id)
    elif message.content_type == "video":
        bot.send_video(chat, message.video.file_id)
    elif message.content_type == "video_note":
        bot.send_video_note(chat, message.video_note.file_id)
    elif message.content_type == "voice":
        bot.send_voice(chat, message.voice.file_id)
    elif message.content_type == "location":
        bot.send_location(chat, message.location.latitude, message.location.longitude)
    elif message.content_type == "contact":
        bot.send_contact(chat, message.contact.phone_number, message.contact.first_name)