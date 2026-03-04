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
        types.InlineKeyboardButton("Salario", callback_data="gain_entry_type_Salario"),
        types.InlineKeyboardButton("VR/VA", callback_data="gain_entry_type_VR/VA"),
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
        "**Qual a forma que você ganhou esse dinheiro?**",
        reply_markup=markup,
        parse_mode="Markdown",
    )


def third_quest_gain(call, finance_bot):
    chat_id = call.message.chat.id
    chat_data[chat_id]["category"] = call.data.replace("gain_entry_type_", "")

    msg = finance_bot.edit_message_text(
        f"Categoria: *{chat_data[chat_id]['category']}*\n\n **Qual o valor**",
        chat_id,
        call.message.message_id,
        parse_mode="Markdown",
    )
    
    finance_bot.register_next_step_handler(msg, fourth_quest_gain, finance_bot)

def fourth_quest_gain(message, finance_bot):
    chat_id = message.chat.id
    chat_data[chat_id]["value"] = message.text.replace(",",".")

    msg = finance_bot.send_message(
        chat_id,
        f"Categoria: *{chat_data[chat_id]['category']}*\n\n *Valor: {chat_data[chat_id]['value']}* \n\n**De onde veio isso? (texto livre)**",
        parse_mode="Markdown",
    )
    
    finance_bot.register_next_step_handler(msg, salvar_final_financeiro, finance_bot)

def salvar_final_financeiro(message,finance_bot):
    chat_id = message.chat.id
    chat_data[chat_id]['description'] = message.text
    
    dados = chat_data[chat_id]
    
    resumo = (
        f"**Novo Registrado!**\n\n"
        f"**Tipo de entrada:** {dados['entry_type']}\n\n"
        f"**Categoria:** {dados['category']}\n"
        f"**Descrição:** {dados['description']}\n"
        f"**Valor:** R$ {dados['value']}\n"
        f"*Dados prontos para o banco de dados!*"
    )
    
    finance_bot.send_message(chat_id, resumo, parse_mode="Markdown")
    finance_bot.send_message(chat_id, "Dados inseridos!", parse_mode="Markdown")
