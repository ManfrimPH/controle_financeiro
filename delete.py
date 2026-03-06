from telebot import types
from data_base import delete

chat_data = {}


def first_quest_del(message, finance_bot):
    chat_id = message.chat.id
    chat_data[chat_id] = {}

    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("Gasto", callback_data="local_spent"),
        types.InlineKeyboardButton("Ganho", callback_data="local_gain"),
    )

    finance_bot.send_message(
        chat_id,
        "**Qual tipo de informação você quer pagar?",
        reply_markup=markup,
        parse_mode="Markdown",
    )


def second_quest_del(call, finance_bot):
    chat_id = call.message.chat.id
    chat_data[chat_id]["local"] = call.data.replace("local_", "")

    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("Sim", callback_data="confirm_Sim"),
        types.InlineKeyboardButton("Não", callback_data="confirm_Não"),
    )

    finance_bot.send_message(
        chat_id,
        "**Você quer mesmo apagar isso?**",
        reply_markup=markup,
        parse_mode="Markdown",
    )


def third_quest_del(call, finance_bot):
    chat_id = call.message.chat.id
    resp = call.data.replace("confirm_", "")

    if resp == "Sim":
        finance_bot.answer_callback_query(call.id, "Processando exclusão...")

        dados = chat_data[chat_id]

        resp_del = delete(dados)

        if resp_del == True:
            finance_bot.send_message(chat_id, "Linha Apagada!", parse_mode="Markdown")
        elif resp_del == False:
            finance_bot.bot.send_message(
                chat_id, "Erro ao Deletar!", parse_mode="Markdown"
            )

    elif resp == "Sao":
        finance_bot.answer_callback_query(call.id)
        finance_bot.edit_message_text(
            chat_id=chat_id,
            message_id=call.message.message_id,
            text="**Operação cancelada.** O registro permanece salvo.",
            parse_mode="Markdown",
        )

    del chat_data[chat_id]
