from telebot import types

chat_data = {}


def first_quest(message, finance_bot):
    chat_id = message.chat.id
    chat_data[chat_id] = {}

    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("Ganhei Dinheiro", callback_data="Ganho"),
        types.InlineKeyboardButton("Gastei Dinheiro", callback_data="Gasto"),
    )

    finance_bot.send_message(
        chat_id,
        "**Novo registro!!** \n O que você fez com seu dinheiro dessa vez?",
        reply_markup=markup,
        parse_mode="Markdown",
    )


## Gain Format


def second_quest_gain(call, finance_bot):
    chat_id = call.message.chat.id
    chat_data[chat_id]["entry_type"] = call.data

    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            "Trabalho", callback_data="gain_entry_type_Trabalho"
        ),
        types.InlineKeyboardButton(
            "Renda Extra", callback_data="gain_entry_type_Renda Extra"
        ),
        types.InlineKeyboardButton(
            "Investimento", callback_data="gain_entry_type_Investimento"
        ),
        types.InlineKeyboardButton(
            "Presente", callback_data="gain_entry_type_Presente"
        ),
    )

    finance_bot.send_message(
        chat_id,
        "**Novo registro!!** \n O que você fez com seu dinheiro dessa vez?",
        reply_markup=markup,
        parse_mode="Markdown",
    )
