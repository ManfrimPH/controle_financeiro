import telebot
import os
from dotenv import load_dotenv
from add import (
    first_quest_add,
    second_quest_gain,
    third_quest_gain,
    second_quest_spent,
    third_quest_spent,
    fourth_quest_spent,
)
from delete import (
    first_quest_del,
    second_quest_del,
    third_quest_del,
)
from update import (
    update
)

load_dotenv()
bot_key = os.getenv("BOT_KEY")

finance_bot = telebot.TeleBot(bot_key)

###########################################################################################
# Addition Flow
###########################################################################################


@finance_bot.message_handler(commands=["add"])
def add_command(message):
    first_quest_add(message, finance_bot)


## Gain quests


@finance_bot.callback_query_handler(
    func=lambda call: call.data.startswith("gain_entry_type_")
)
def add_callback_gain_one(call):
    second_quest_gain(call, finance_bot)


@finance_bot.callback_query_handler(
    func=lambda call: call.data.startswith("gain_category_")
)
def add_callback_gain_two(call):
    third_quest_gain(call, finance_bot)


## Spent quests


@finance_bot.callback_query_handler(
    func=lambda call: call.data.startswith("spent_entry_type_")
)
def add_callback_spent_one(call):
    second_quest_spent(call, finance_bot)


@finance_bot.callback_query_handler(
    func=lambda call: call.data.startswith("spent_category_")
)
def add_callback_spent_two(call):
    third_quest_spent(call, finance_bot)


@finance_bot.callback_query_handler(
    func=lambda call: call.data.startswith("spent_payment_method_")
)
def add_callback_spent_three(call):
    fourth_quest_spent(call, finance_bot)


###########################################################################################
# Deletion Flow
###########################################################################################


@finance_bot.message_handler(commands=["del"])
def del_command(message):
    first_quest_del(message, finance_bot)


@finance_bot.callback_query_handler(func=lambda call: call.data.startswith("local_"))
def add_callback_del_one(call):
    second_quest_del(call, finance_bot)


@finance_bot.callback_query_handler(func=lambda call: call.data.startswith("confirm_"))
def add_callback_del_two(call):
    third_quest_del(call, finance_bot)


###########################################################################################
# Update Flow
###########################################################################################

@finance_bot.message_handler(commands=["update"])
def update_system(message):
    tables = ["gain", "spent"]
    for table in tables:
        update(table)

finance_bot.infinity_polling()
