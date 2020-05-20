from timezonefinder import TimezoneFinder

from add import listreminders, telegramcalendar
from add.database import Database
from add.formatdate import FormatDate
from add.type import record
from add.type import view_name, number_of_reminder


editText = (False, None)
editDate = (False, None)


def bot(bot):
    """
    processes user requests using the telebot library
    :param telebot.TeleBot bot:
    :return: nothing
    """
    global editText

    local_memory = {}

    calendar_data = ["IGNORE", "DAY", "PREV-MONTH", "NEXT-MONTH"]

    @bot.message_handler(commands=['start'])
    def start_message(message):
        """the start message"""
        db = Database('db')
        if not db.show("user", ID=str(message.chat.id)):
            db.add(table="user", ID=str(message.chat.id), TIMEZONE="'UTC'")
        bot.send_message(message.from_user.id, "Enter '/reminder' to set a reminder.")

    @bot.message_handler(commands=['remind_list'])
    def remind_list(message):
        """menu for managing reminders"""
        db = Database('db')
        if db.show("message", ID=str(message.chat.id)):
            bot.send_message(message.from_user.id, "please select reminder:",
                             reply_markup=listreminders.create_list(db.show(table="message", ID=message.chat.id)))
        else:
            bot.send_message(message.from_user.id, "You haven't reminder")

    @bot.message_handler(commands=['timezone'])
    def start_timezone(message):
        """send message about setting the timezone"""
        msg = bot.send_message(message.from_user.id, 'please send your location')
        bot.register_next_step_handler(msg, set_timezone)

    def set_timezone(message):
        """setting the timezone"""
        db = Database('db')
        if message.content_type == "location":
            tf = TimezoneFinder()
            timezone = tf.timezone_at(lng=message.location.longitude, lat=message.location.latitude)

            if db.show(table="user", ID=str(message.chat.id)):
                db.edit(table="user", values={"TIMEZONE": f"'{timezone}'"}, ID=str(message.chat.id))
            else:
                db.add(table="user", ID=str(message.chat.id), TIMEZONE=f"'{timezone}'")

            bot.send_message(message.from_user.id, f"Your timezone is {timezone}")

        else:
            msg = bot.send_message(message.from_user.id, "You didn't send your location")
            bot.register_next_step_handler(msg, set_timezone)

    @bot.message_handler(commands=['cancel_all'])
    def cancel_all_message(message):
        """cancel all reminder"""
        db = Database('db')
        db.remove(table='message', ID=str(message.chat.id))
        bot.send_message(message.from_user.id, "All reminders were cancelled.")

    @bot.message_handler(commands=['reminder'])
    def reminder_handler(message):
        """send message about setting the reminder"""
        db = Database('db')
        if message.chat.id not in local_memory:
            local_memory[message.chat.id] = {}

        if not db.show("user", ID=str(message.chat.id)):
            db.add(table="user", ID=str(message.chat.id), TIMEZONE="'UTC'")

        msg = bot.send_message(message.from_user.id, 'please enter the message')
        bot.register_next_step_handler(msg, message_handler)

    def message_handler(message):
        """show calendar for select of date and setting message of reminder"""
        global editText
        db = Database('db')

        if not editText[0]:
            local_memory[message.chat.id]["messages"] = message
            bot.send_message(message.from_user.id, "choose date:",
                             reply_markup=telegramcalendar.create_calendar())
        else:
            db.edit(table='message',
                    values={"MESSAGE1": f"'{record(message)[0]}'", "MESSAGE2": f"'{record(message)[1]}'",
                            "SHOW_MESSAGE": f"'{view_name(message)}'"}, NUMBER=editText[1])
            bot.send_message(message.from_user.id, "reminder was edited")
        editText = (False, None)

    @bot.callback_query_handler(func=lambda call: call.data.split(";")[0] in calendar_data)
    def callback_calendar(call):
        """setting date of reminder"""
        global editDate
        db = Database('db')
        selected, date2, time_sending = telegramcalendar.process_calendar_selection(bot, call, db)

        if selected:
            bot.send_message(call.from_user.id, "You selected %s" % (date2.strftime("%d.%m.%Y")))
            if not editDate[0]:
                number = number_of_reminder(
                    db.show(table='message', show_column='NUMBER', ID=str(call.message.chat.id)))
                for date in time_sending:

                    db.add(table="message", ID=str(call.message.chat.id),
                           DATE=f"'{FormatDate(date, '%Y/%M/%D/%h/%m/%s')}'",
                           TYPE=f"'{local_memory[call.message.chat.id]['messages'].content_type}'",
                           MESSAGE1=f"'{record(local_memory[call.message.chat.id]['messages'])[0]}'",
                           MESSAGE2=f"'{record(local_memory[call.message.chat.id]['messages'])[1]}'",
                           SHOW_MESSAGE=f"'{view_name(local_memory[call.message.chat.id]['messages'])}'",
                           NUMBER=f"{number}")

                local_memory.pop(call.message.chat.id)
            else:
                for date in time_sending:
                    db.edit(table="message", values={"DATE": f"'{FormatDate(date, '%Y/%M/%D/%h/%m/%s')}'"},
                            NUMBER=editDate[1], ID=call.message.chat.id)

                editDate = (False, None)

    @bot.callback_query_handler(func=lambda call: call.data.split(";")[-1] == "1")
    def reminder_list(call):
        """show menu for edit the reminder"""
        listreminders.processing_selected_reminder(bot, call)

    @bot.callback_query_handler(func=lambda call: call.data.split(";")[-1] == "2")
    def option_menu(call):
        """delete the reminder or show edit menu"""
        db = Database('db')
        action, number, reminder, step = call.data.split(";")
        if action == "DELETE":
            db.remove(table='message', ID=call.message.chat.id, NUMBER=number)
            bot.send_message(chat_id=call.message.chat.id, text="message was delete")
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        else:
            listreminders.processing_selected_option(bot, call)

    @bot.callback_query_handler(func=lambda call: call.data.split(";")[-1] == "3")
    def edit(call):
        """edit the content of reminder"""
        global editText
        global editDate

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
