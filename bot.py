from timezonefinder import TimezoneFinder

from add import listreminders, telegramcalendar
from add.formatdate import FormatDate
from add.type import record
from add.type import view_name, number_of_reminder

editText = (False, None)
editDate = (False, None)


def bot(bot, db):
    """
    processes user requests using the telebot library
    :param telebot.TeleBot bot:
    :param Database db:
    :return: nothing
    """
    global editText

    local_memory = {}

    calendar_data = ["IGNORE", "DAY", "PREV-MONTH", "NEXT-MONTH"]

    def update_user(id):
        db.connect()
        if not db.select(table='users', id=str(id)):
            db.add(table='users', id=str(id), timezone="'UTC'", language='en')

    @bot.message_handler(commands=['start'])
    def start_message(message):
        """the start message"""
        update_user(message.chat.id)

        bot.send_message(message.from_user.id, "Enter '/reminder' to set a reminder.")

    @bot.message_handler(commands=['remind_list'])
    def remind_list(message):
        """menu for managing reminders"""
        update_user(message.chat.id)

        if db.select("messages", user_id=str(message.chat.id)):
            bot.send_message(message.from_user.id, "please select reminder:",
                             reply_markup=listreminders.create_list(db.select(table="messages",
                                                                              user_id=message.chat.id)))
        else:
            bot.send_message(message.from_user.id, "You haven't reminder")

    @bot.message_handler(commands=['timezone'])
    def start_timezone(message):
        """send message about setting the timezone"""
        update_user(message.chat.id)

        msg = bot.send_message(message.from_user.id, 'please send your location')
        bot.register_next_step_handler(msg, set_timezone)

    def set_timezone(message):
        """setting the timezone"""
        update_user(message.chat.id)

        if message.content_type == "location":
            tf = TimezoneFinder()
            timezone = tf.timezone_at(lng=message.location.longitude, lat=message.location.latitude)

            db.edit(table="users", values={"timezone": f"'{timezone}'"}, id=str(message.chat.id))

            bot.send_message(message.from_user.id, f"Your timezone is {timezone}")

        else:
            msg = bot.send_message(message.from_user.id, "You didn't send your location")
            bot.register_next_step_handler(msg, set_timezone)

    @bot.message_handler(commands=['cancel_all'])
    def cancel_all_message(message):
        """cancel all reminder"""
        update_user(message.chat.id)

        db.remove(table='messages', user_id=str(message.chat.id))
        bot.send_message(message.from_user.id, "All reminders were cancelled.")

    @bot.message_handler(commands=['reminder'])
    def reminder_handler(message):
        """send message about setting the reminder"""
        update_user(message.chat.id)

        if message.chat.id not in local_memory:
            local_memory[message.chat.id] = {}

        if not db.select("users", id=str(message.chat.id)):
            db.add(table="users", id=str(message.chat.id), timezone="'UTC'")

        msg = bot.send_message(message.from_user.id, 'please enter the message')
        bot.register_next_step_handler(msg, message_handler)

    def message_handler(message):
        """show calendar for select of date and setting message of reminder"""
        global editText
        update_user(message.chat.id)

        if not editText[0]:
            local_memory[message.chat.id]["messages"] = message
            bot.send_message(message.from_user.id, "choose date:",
                             reply_markup=telegramcalendar.create_calendar())
        else:
            db.edit(table='messages',
                    values={"message1": f"'{record(message)[0]}'", "message2": f"'{record(message)[1]}'",
                            "description": f"'{view_name(message)}'"}, id=editText[1])
            bot.send_message(message.from_user.id, "reminder was edited")
        editText = (False, None)

    @bot.callback_query_handler(func=lambda call: call.data.split(";")[0] in calendar_data)
    def callback_calendar(call):
        """setting date of reminder"""
        global editDate
        update_user(call.message.chat.id)

        selected, date2, time_sending = telegramcalendar.process_calendar_selection(bot, call, db)

        if selected:
            bot.send_message(call.from_user.id, "You selected %s" % (date2.strftime("%d.%m.%Y")))
            if not editDate[0]:
                number = number_of_reminder(
                    db.select(table='messages', column='id', user_id=str(call.message.chat.id)))
                for date in time_sending:

                    db.add(table="messages", user_id=str(call.message.chat.id),
                           date=f"'{FormatDate(date, '%Y/%M/%D/%h/%m/%s')}'",
                           type=f"'{local_memory[call.message.chat.id]['messages'].content_type}'",
                           message1=f"'{record(local_memory[call.message.chat.id]['messages'])[0]}'",
                           message2=f"'{record(local_memory[call.message.chat.id]['messages'])[1]}'",
                           description=f"'{view_name(local_memory[call.message.chat.id]['messages'])}'",
                           id=f"{number}")

                local_memory.pop(call.message.chat.id)
            else:
                for date in time_sending:
                    db.edit(table="messages", values={"date": f"'{FormatDate(date, '%Y/%M/%D/%h/%m/%s')}'"},
                            id=editDate[1], user_id=call.message.chat.id)

                editDate = (False, None)

    @bot.callback_query_handler(func=lambda call: call.data.split(";")[-1] == "1")
    def reminder_list(call):
        """show menu for edit the reminder"""
        listreminders.processing_selected_reminder(bot, call)

    @bot.callback_query_handler(func=lambda call: call.data.split(";")[-1] == "2")
    def option_menu(call):
        """delete the reminder or show edit menu"""
        update_user(call.message.chat.id)

        action, number, reminder, step = call.data.split(";")
        if action == "DELETE":
            db.remove(table='messages', user_id=call.message.chat.id, id=number)
            bot.send_message(chat_id=call.message.chat.id, text="message was delete")
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        else:
            listreminders.processing_selected_option(bot, call)

    @bot.callback_query_handler(func=lambda call: call.data.split(";")[-1] == "3")
    def edit(call):
        """edit the content of reminder"""
        global editText
        global editDate

        update_user(call.message.chat.id)

        action, number, step = call.data.split(";")

        if action == "EDIT_TEXT":
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            editText = (True, number)
            msg = bot.send_message(call.message.chat.id, 'please enter the message')
            bot.register_next_step_handler(msg, message_handler)

        elif action == "EDIT_DATE":
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            editDate = (True, number)
            bot.send_message(call.message.chat.id, "choose date:", reply_markup=telegramcalendar.create_calendar())
        elif action == "CANCEL":
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

    bot.polling(none_stop=True, interval=0)
