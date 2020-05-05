import pytz
from telebot.types import ReplyKeyboardRemove
from timezonefinder import TimezoneFinder

import telegramcalendar

base_memory = {}
timezone_list = {}


def bot(bot):
    global timezone_list
    global base_memory
    local_memory = {}
    messages = []
    date = []
    d_timezone = pytz.timezone("UTC")

    @bot.message_handler(commands=['start'])
    def start_message(message):
        if message.chat.id not in timezone_list:
            timezone_list[message.chat.id] = d_timezone
        bot.send_message(message.from_user.id, "Enter '/reminder' to set a reminder.")

    @bot.message_handler(commands=['timezone'])
    def timezone(message):
        msg = bot.send_message(message.from_user.id, 'please send your location')
        bot.register_next_step_handler(msg, set_timezone)

    def set_timezone(message):
        global timezone_list
        if message.content_type == "location":
            tf = TimezoneFinder()
            timezone = tf.timezone_at(lng=message.location.longitude, lat=message.location.latitude)
            timezone_list[message.chat.id] = pytz.timezone(timezone)
            bot.send_message(message.from_user.id, f"Your timezone is {timezone}.")

        else:
            msg = bot.send_message(message.from_user.id, "You didn't send your location")
            bot.register_next_step_handler(msg, set_timezone)

    @bot.message_handler(commands=['cancel_last'])
    def cancel_last_message(message):
        global base_memory
        bot.send_message(message.from_user.id, "Last reminder was cancelled.")
        if message.from_user.id in base_memory:
            base_memory[message.from_user.id]["messages"].pop()
            base_memory[message.from_user.id]["date"].pop()

    @bot.message_handler(commands=['cancel_all'])
    def cancel_all_message(message):
        global base_memory
        bot.send_message(message.from_user.id, "All reminders were cancelled.")
        if message.chat.id in local_memory:
            base_memory.pop(message.chat.id)

    @bot.message_handler(commands=['reminder'])
    def reminder_message(message):
        global base_memory
        global timezone_list
        if message.chat.id not in local_memory:
            local_memory[message.chat.id] = {"messages": messages.copy(), "date": date.copy()}
        if message.chat.id not in timezone_list:
            timezone_list[message.chat.id] = d_timezone

        msg = bot.send_message(message.from_user.id, 'please enter the message')
        bot.register_next_step_handler(msg, text_messages)

    def text_messages(message):
        global timezone_list
        if message.chat.id not in local_memory:
            local_memory[message.chat.id] = {"messages": messages.copy(), "date": date.copy()}
        if message.chat.id not in timezone_list:
            timezone_list[message.chat.id] = d_timezone
        local_memory[message.chat.id]["messages"].append(message)
        bot.send_message(message.from_user.id, "choose date:", reply_markup=telegramcalendar.create_calendar())

    @bot.callback_query_handler(func=lambda
            call: call.data == "IGNORE" or call.data == "DAY" or call.data == "PREV-MONTH" or call.data == "NEXT-MONTH")
    def callback_query(call):
        global base_memory
        global timezone_list
        if call.message.chat.id not in local_memory:
            local_memory[call.message.chat.id] = {"messages": messages.copy(), "date": date.copy()}
        if call.message.chat.id not in timezone_list:
            timezone_list[call.message.chat.id] = d_timezone

        selected, date2, time_sending = telegramcalendar.process_calendar_selection(bot, call)
        if selected:
            local_memory[call.message.chat.id]["date"].append(time_sending)
            bot.send_message(call.from_user.id, "You selected %s" % (date2.strftime("%d/%m/%Y")),
                             reply_markup=ReplyKeyboardRemove())
        base_memory = local_memory.copy()

    bot.polling(none_stop=True, interval=0)
