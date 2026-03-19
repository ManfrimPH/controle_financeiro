from telebot import types
from data_base import add_gain, add_spent

chat_data = {}


def first_quest_add(message, finance_bot):
    chat_id = message.chat.id
    chat_data[chat_id] = {}

    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton(
            "Ganhei Dinheiro", callback_data="gain_entry_type_Ganho"
        ),
        types.InlineKeyboardButton(
            "Gastei Dinheiro", callback_data="spent_entry_type_Gasto"
        ),
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
    chat_data[chat_id]["entry_type"] = call.data.replace("gain_entry_type_", "")

    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("Salario", callback_data="gain_category_Salario"),
        types.InlineKeyboardButton("VR/VA", callback_data="gain_category_VR/VA"),
        types.InlineKeyboardButton(
            "Renda Extra", callback_data="gain_category_Renda Extra"
        ),
        types.InlineKeyboardButton(
            "Investimento", callback_data="gain_category_Investimento"
        ),
        types.InlineKeyboardButton("Presente", callback_data="gain_category_Presente"),
    )

    finance_bot.send_message(
        chat_id,
        "**Qual a forma que você ganhou esse dinheiro?**",
        reply_markup=markup,
        parse_mode="Markdown",
    )


def third_quest_gain(call, finance_bot):
    chat_id = call.message.chat.id
    chat_data[chat_id]["category"] = call.data.replace("gain_category_", "")

    msg = finance_bot.edit_message_text(
        f"Categoria: *{chat_data[chat_id]['category']}*\n\n **Qual o valor**",
        chat_id,
        call.message.message_id,
        parse_mode="Markdown",
    )

    finance_bot.register_next_step_handler(msg, fourth_quest_gain, finance_bot)


def fourth_quest_gain(message, finance_bot):
    chat_id = message.chat.id
    chat_data[chat_id]["value"] = message.text.replace(",", ".")

    msg = finance_bot.send_message(
        chat_id,
        f"Categoria: *{chat_data[chat_id]['category']}*\n\n *Valor: {chat_data[chat_id]['value']}* \n\n**De onde veio isso? (texto livre)**",
        parse_mode="Markdown",
    )

    finance_bot.register_next_step_handler(msg, fifth_quest_gain, finance_bot)


def fifth_quest_gain(message, finance_bot):

    chat_id = message.chat.id
    chat_data[chat_id]["description"] = message.text

    msg = finance_bot.send_message(
        chat_id,
        "**Para qual data é esse gasto?**\nResponda (DD/MM/AAAA).",
        parse_mode="Markdown"
    )

    finance_bot.register_next_step_handler(msg, save_gain, finance_bot)

def save_gain(message, finance_bot):
    chat_id = message.chat.id
    chat_data[chat_id]["date"] = message.text

    dados = chat_data[chat_id]

    resumo = (
        f"**Novo Registrado!**\n\n"
        f"**Tipo de entrada:** {dados['entry_type']}\n\n"
        f"**Categoria:** {dados['category']}\n"
        f"**Descrição:** {dados['description']}\n"
        f"**Valor:** R$ {dados['value']}\n"
        f"**Data:** {dados['date']}\n"
        f"*Dados prontos para o banco de dados!*"
    )

    finance_bot.send_message(chat_id, resumo, parse_mode="Markdown")

    resp = add_gain(dados)

    if resp == True:
        finance_bot.send_message(chat_id, "Dados inseridos!", parse_mode="Markdown")
    elif resp == False:
        finance_bot.bot.send_message(chat_id, "Erro ao inserir!", parse_mode="Markdown")

    del chat_data[chat_id]


## Spent Format


def second_quest_spent(call, finance_bot):
    chat_id = call.message.chat.id
    chat_data[chat_id]["entry_type"] = call.data.replace("spent_entry_type_", "")

    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            "Essencial", callback_data="spent_category_Essencial"
        ),
        types.InlineKeyboardButton(
            "Estilo de Vida", callback_data="spent_category_Estilo de Vida"
        ),
        types.InlineKeyboardButton(
            "Investimento e Projetos",
            callback_data="spent_category_Investimento e Projetos",
        ),
        types.InlineKeyboardButton(
            "Besteiras", callback_data="spent_category_Besteiras"
        ),
        types.InlineKeyboardButton("Lazer", callback_data="spent_category_Lazer"),
    )

    finance_bot.send_message(
        chat_id,
        "**Com que tipo de coisas você gastou esse dinheiro?**",
        reply_markup=markup,
        parse_mode="Markdown",
    )


def third_quest_spent(call, finance_bot):
    chat_id = call.message.chat.id
    chat_data[chat_id]["category"] = call.data.replace("spent_category_", "")

    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            "Debito", callback_data="spent_payment_method_Debito"
        ),
        types.InlineKeyboardButton("VR/VA", callback_data="spent_payment_method_VR/VA"),
        types.InlineKeyboardButton(
            "Credito", callback_data="spent_payment_method_Credito"
        ),
    )

    finance_bot.send_message(
        chat_id,
        "**Como foi que você pagou por isso?**",
        reply_markup=markup,
        parse_mode="Markdown",
    )


def fourth_quest_spent(call, finance_bot):
    chat_id = call.message.chat.id
    chat_data[chat_id]["payment_method"] = call.data.replace(
        "spent_payment_method_", ""
    )

    msg = finance_bot.edit_message_text(
        f"Categoria: *{chat_data[chat_id]['category']}*\n\n Categoria: *{chat_data[chat_id]['payment_method']}*\n\n **Qual o valor?**",
        chat_id,
        call.message.message_id,
        parse_mode="Markdown",
    )

    finance_bot.register_next_step_handler(msg, fifth_quest_spent, finance_bot)


def fifth_quest_spent(message, finance_bot):
    chat_id = message.chat.id
    chat_data[chat_id]["value"] = message.text.replace(",", ".")

    msg = finance_bot.send_message(
        chat_id,
        f"Categoria: *{chat_data[chat_id]['category']}*\n\n Categoria: *{chat_data[chat_id]['payment_method']}*\n\n *Valor: {chat_data[chat_id]['value']}* \n\n**No que foi esse gasto? (texto livre)**",
        parse_mode="Markdown",
    )

    finance_bot.register_next_step_handler(msg, sixth_quest_gain, finance_bot)


def sixth_quest_gain(message, finance_bot):

    chat_id = message.chat.id
    chat_data[chat_id]["description"] = message.text

    msg = finance_bot.send_message(
        chat_id,
        "**Para qual data é esse gasto?**\nResponda (DD/MM/AAAA).",
        parse_mode="Markdown"
    )

    finance_bot.register_next_step_handler(msg, save_spent, finance_bot)


def save_spent(message, finance_bot):
    chat_id = message.chat.id
    chat_data[chat_id]["date"] = message.text

    dados = chat_data[chat_id]

    resumo = (
        f"**Novo Registrado!**\n\n"
        f"**Tipo de entrada:** {dados['entry_type']}\n\n"
        f"**Método de pagamento:** {dados['payment_method']}\n"
        f"**Categoria:** {dados['category']}\n"
        f"**Descrição:** {dados['description']}\n"
        f"**Valor:** R$ {dados['value']}\n"
        f"**Data:** {dados['date']}\n"
        f"*Dados prontos para o banco de dados!*"
    )

    finance_bot.send_message(chat_id, resumo, parse_mode="Markdown")

    resp = add_spent(dados)

    if resp == True:
        finance_bot.send_message(chat_id, "Dados inseridos!", parse_mode="Markdown")
    elif resp == False:
        finance_bot.bot.send_message(chat_id, "Erro ao inserir!", parse_mode="Markdown")

    del chat_data[chat_id]
