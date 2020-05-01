from datetime import timedelta

from telebot.types import ReplyKeyboardRemove, Message, PhotoSize

import telegramcalendar

base_memory = {}


def bot(bot):
    global base_memory

    local_memory = {}
    safe_memory = {}
    messages = []
    date = []

    @bot.message_handler(commands=['start'])
    def start_message(message):
        bot.send_message(message.from_user.id, "Enter '/reminder' to set a reminder.")

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
        if message.chat.id not in local_memory:
            local_memory[message.chat.id] = {"messages": messages.copy(), "date": date.copy()}

        msg = bot.send_message(message.from_user.id, 'please enter the message')
        bot.register_next_step_handler(msg, text_messages)

    def text_messages(message):
        if message.chat.id not in local_memory:
            local_memory[message.chat.id] = {"messages": messages.copy(), "date": date.copy()}
        local_memory[message.chat.id]["messages"].append(message)
        bot.send_message(message.from_user.id, "choose date:", reply_markup=telegramcalendar.create_calendar())

    @bot.callback_query_handler(func=lambda call: True)
    def callback_query(call):
        global base_memory
        if call.message.chat.id not in local_memory:
            local_memory[call.message.chat.id] = {"messages": messages.copy(), "date": date.copy()}

        selected, date2 = telegramcalendar.process_calendar_selection(bot, call)
        if selected:
            local_memory[call.message.chat.id]["date"].append(date2 + timedelta(minutes=2))
            bot.send_message(call.from_user.id, "You selected %s" % (date2.strftime("%d/%m/%Y")),
                             reply_markup=ReplyKeyboardRemove())
        base_memory = local_memory.copy()
    bot.polling(none_stop=True, interval=0)
