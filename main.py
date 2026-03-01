import telebot
import os
from dotenv import load_dotenv
from add import first_quest,second_quest

load_dotenv()
bot_key = os.getenv('BOT_KEY')

finance_bot = telebot.TeleBot(bot_key)

@finance_bot.message_handler(commands=['add'])
def add_command(message):
  first_quest(message,finance_bot)

## Gain quests

@finance_bot.callback_query_handler(func=lambda call: call.data.startswith('Ganho'))
def add_callback_one(call):
  second_quest_gain(call,finance_bot)



## Spent quests

@finance_bot.callback_query_handler(func=lambda call: call.data.startswith('Gasto'))
def add_callback_one(call):
  second_quest_spent(call,finance_bot)



finance_bot.polling()