import datetime
import logging
import traceback

import pytz
from timezonefinder import TimezoneFinder

import listreminders
import telegramcalendar
from formatdate import FormatDate

base_memory = {}
timezone_list = {}
editText = False


def bot(bot):
    """

    :param telebot.TeleBot bot:
    :return:
    """

    global editText
    global timezone_list
    global base_memory
    message_about_error = [970352590]

    local_memory = {}
    messages = []
    date = []

    calendar_data = ["IGNORE", "DAY", "PREV-MONTH", "NEXT-MONTH"]
    option_list = ["CANCEL", "EDIT", "DELETE"]
    edit_list = ["EDIT_TEXT", "EDIT_DATE"]

    d_timezone = pytz.timezone("UTC")
    logging.basicConfig(filename="mySnake.log",
                        format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                        level=logging.DEBUG)

    def delete(message_id, index):
        """delete message"""
        global base_memory
        if message_id in base_memory:
            base_memory[message_id]["messages"].pop(int(index))
            base_memory[message_id]["date"].pop(int(index))
            if not base_memory[message_id]["messages"]:
                base_memory.pop(message_id)

    @bot.message_handler(commands=['start'])
    def start_message(message):
        """the start message"""
        if message.chat.id not in timezone_list:
            timezone_list[message.chat.id] = d_timezone
        bot.send_message(message.from_user.id, "Enter '/reminder' to set a reminder.")

    @bot.message_handler(commands=['now'])
    def now(message):
        global timezone_list

        if message.chat.id not in timezone_list:
            timezone_list[message.chat.id] = d_timezone

        bot.send_message(message.from_user.id,
                         FormatDate(
                             datetime.datetime.now(tz=timezone_list[message.chat.id]).replace(tzinfo=None),
                             "%D/%M/%Y %h:%m:%s"))
        f = "2"/2

    @bot.message_handler(commands=['remind_list'])
    def remind_list(message):
        """menu for managing reminders"""
        global base_memory
        if message.chat.id in base_memory:
            bot.send_message(message.from_user.id, "please select reminder:",
                             reply_markup=listreminders.create_list(base_memory[message.chat.id]["messages"],
                                                                    base_memory[message.chat.id]["date"]))
        else:
            bot.send_message(message.from_user.id, "You haven't reminder")

    @bot.message_handler(commands=['timezone'])
    def timezone(message):
        """send message about setting the timezone"""
        msg = bot.send_message(message.from_user.id, 'please send your location')
        bot.register_next_step_handler(msg, set_timezone)

    def set_timezone(message):
        """setting the timezone"""
        global timezone_list
        if message.content_type == "location":
            tf = TimezoneFinder()
            timezone = tf.timezone_at(lng=message.location.longitude, lat=message.location.latitude)
            timezone_list[message.chat.id] = pytz.timezone(timezone)
            bot.send_message(message.from_user.id, f"Your timezone is {timezone}.")

        else:
            msg = bot.send_message(message.from_user.id, "You didn't send your location")
            bot.register_next_step_handler(msg, set_timezone)

    @bot.message_handler(commands=['cancel_all'])
    def cancel_all_message(message):
        """cancel all reminder"""
        global base_memory
        bot.send_message(message.from_user.id, "All reminders were cancelled.")
        if message.chat.id in local_memory:
            base_memory.pop(message.chat.id)

    @bot.message_handler(commands=['reminder'])
    def reminder_handler(message):
        """reminder handler"""
        global base_memory
        global timezone_list
        if message.chat.id not in local_memory:
            local_memory[message.chat.id] = {"messages": messages.copy(), "date": date.copy()}
        if message.chat.id not in timezone_list:
            timezone_list[message.chat.id] = d_timezone

        msg = bot.send_message(message.from_user.id, 'please enter the message')
        bot.register_next_step_handler(msg, message_handler)

    @bot.message_handler(commands=['chat_id'])
    def chat_id(message):
        bot.send_message(message.chat.id, str(message.chat.id))

    def message_handler(message):
        """message handler"""
        global timezone_list
        global editText
        if message.chat.id not in local_memory:
            local_memory[message.chat.id] = {"messages": messages.copy(), "date": date.copy()}
        if message.chat.id not in timezone_list:
            timezone_list[message.chat.id] = d_timezone
        local_memory[message.chat.id]["messages"].append(message)
        if not editText:
            bot.send_message(message.from_user.id, "choose date:",
                             reply_markup=telegramcalendar.create_calendar())
        else:
            bot.send_message(message.from_user.id, "reminder was edited")
        editText = False

    @bot.callback_query_handler(func=lambda call: call.data.split(";")[0] in calendar_data)
    def callback_query(call):
        """calendar button click handler"""
        global base_memory
        global timezone_list
        if call.message.chat.id not in local_memory:
            local_memory[call.message.chat.id] = {"messages": messages.copy(), "date": date.copy()}
        if call.message.chat.id not in timezone_list:
            timezone_list[call.message.chat.id] = d_timezone

        selected, date2, time_sending = telegramcalendar.process_calendar_selection(bot, call)

        if selected:
            local_memory[call.message.chat.id]["date"].append(time_sending)
            bot.send_message(call.from_user.id, "You selected %s" % (date2.strftime("%d.%m.%Y")))
            base_memory = local_memory.copy()

    @bot.callback_query_handler(
        func=lambda call: len(call.data.split(";")) == 3 and call.data.split(";")[2] == "list")
    def reminder_list(call):
        """list of reminders click handler"""
        listreminders.process_reminder_selection(bot, call)

    @bot.callback_query_handler(func=lambda call: call.data.split(";")[0] in option_list)
    def option_menu(call):
        """option button click handler"""
        global base_memory
        action, index, reminder = call.data.split(";")
        if action == "DELETE":
            delete(call.message.chat.id, index)
            bot.send_message(chat_id=call.message.chat.id, text="message was delete")
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        else:
            listreminders.process_option_selection(bot, call)

    @bot.callback_query_handler(func=lambda call: call.data.split(";")[0] in edit_list)
    def edit(call):
        global editText
        action, index = call.data.split(";")
        local_memory[call.message.chat.id]["date"].append(
            local_memory[call.message.chat.id]["date"][int(index)])
        local_memory[call.message.chat.id]["messages"].append(
            local_memory[call.message.chat.id]["messages"][int(index)])
        delete(call.message.chat.id, index)

        if action == "EDIT_TEXT":
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            local_memory[call.message.chat.id]["messages"].pop()
            editText = True
            msg = bot.send_message(call.message.chat.id, 'please enter the message')
            bot.register_next_step_handler(msg, message_handler)

        elif action == "EDIT_DATE":
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            local_memory[call.message.chat.id]["date"].pop()
            bot.send_message(call.message.chat.id, "choose date:",
                             reply_markup=telegramcalendar.create_calendar())
        elif action == "CANCEL":
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

    try:
        bot.polling(none_stop=True, interval=0)
    except Exception:
        for i in message_about_error:
            bot.send_message(i, f"error: \n {traceback.format_exc()}")
