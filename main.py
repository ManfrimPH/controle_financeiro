import telebot
import os
import logging
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
from update import update
from conversation import conv_manager
from commands import cmd_list, cmd_summary

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("finance_bot")

load_dotenv()
bot_key = os.getenv("BOT_KEY")

finance_bot = telebot.TeleBot(bot_key)

# Set up command menu
COMMANDS = [
    ("add", "Registrar ganho ou gasto"),
    ("del", "Apagar ultimo registro"),
    ("list", "Mostrar ultimos registros"),
    ("summary", "Resumo mensal do mes"),
    ("update", "Sincronizar com Google Sheets"),
    ("cancel", "Cancelar operacao atual"),
]
try:
    finance_bot.set_my_commands(
        [telebot.types.BotCommand(cmd, desc) for cmd, desc in COMMANDS]
    )
    logger.info("Bot commands registered")
except Exception as e:
    logger.warning("Could not register commands: %s", e)


@finance_bot.message_handler(commands=["cancel"])
def cancel_command(message):
    chat_id = message.chat.id
    conv_manager.cleanup(chat_id)
    finance_bot.send_message(
        chat_id, "Operacao cancelada. Nada foi salvo.",
        parse_mode="Markdown",
    )


@finance_bot.message_handler(commands=["add"])
def add_command(message):
    conv_manager.create(message.chat.id, "add")
    first_quest_add(message, finance_bot)


@finance_bot.callback_query_handler(
    func=lambda call: call.data.startswith("gain_entry_type_")
)
def add_callback_gain_one(call):
    conv_manager.touch(call.message.chat.id)
    second_quest_gain(call, finance_bot)


@finance_bot.callback_query_handler(
    func=lambda call: call.data.startswith("gain_category_")
)
def add_callback_gain_two(call):
    conv_manager.touch(call.message.chat.id)
    third_quest_gain(call, finance_bot)


@finance_bot.callback_query_handler(
    func=lambda call: call.data.startswith("spent_entry_type_")
)
def add_callback_spent_one(call):
    conv_manager.touch(call.message.chat.id)
    second_quest_spent(call, finance_bot)


@finance_bot.callback_query_handler(
    func=lambda call: call.data.startswith("spent_category_")
)
def add_callback_spent_two(call):
    conv_manager.touch(call.message.chat.id)
    third_quest_spent(call, finance_bot)


@finance_bot.callback_query_handler(
    func=lambda call: call.data.startswith("spent_payment_method_")
)
def add_callback_spent_three(call):
    conv_manager.touch(call.message.chat.id)
    fourth_quest_spent(call, finance_bot)


@finance_bot.message_handler(commands=["del"])
def del_command(message):
    conv_manager.create(message.chat.id, "del")
    first_quest_del(message, finance_bot)


@finance_bot.callback_query_handler(func=lambda call: call.data.startswith("local_"))
def add_callback_del_one(call):
    conv_manager.touch(call.message.chat.id)
    second_quest_del(call, finance_bot)


@finance_bot.callback_query_handler(func=lambda call: call.data.startswith("confirm_"))
def add_callback_del_two(call):
    conv_manager.touch(call.message.chat.id)
    third_quest_del(call, finance_bot)


@finance_bot.message_handler(commands=["update"])
def update_system(message):
    tables = ["gain", "spent"]
    for table in tables:
        update(table)
    finance_bot.send_message(
        message.chat.id,
        "Planilha atualizada com sucesso!",
        parse_mode="Markdown",
    )


@finance_bot.message_handler(commands=["list"])
def list_command(message):
    cmd_list(message, finance_bot)


@finance_bot.message_handler(commands=["summary"])
def summary_command(message):
    cmd_summary(message, finance_bot)


if __name__ == "__main__":
    logger.info("Bot started")
    finance_bot.infinity_polling()
