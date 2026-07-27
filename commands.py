from datetime import datetime
from decimal import Decimal
from telebot import types
import db

MONTH_NAMES = [
    "", "Janeiro", "Fevereiro", "Marco", "Abril", "Maio", "Junho",
    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro",
]


def _fmt(value: Decimal) -> str:
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def cmd_list(message, finance_bot):
    chat_id = message.chat.id
    gain_rows, _ = db.get_last("gain", 5)
    spent_rows, _ = db.get_last("spent", 5)
    lines = ["**Ultimos registros**\n"]
    if gain_rows:
        lines.append("**Ganhos:**")
        for row in gain_rows:
            _, cat, val, desc, dt, _ = row
            lines.append(f"  {_fmt(val)} | {cat} | {dt.strftime('%d/%m')}")
    else:
        lines.append("Nenhum ganho registrado.")
    lines.append("")
    if spent_rows:
        lines.append("**Gastos:**")
        for row in spent_rows:
            _, cat, pm, val, desc, dt, _ = row
            lines.append(f"  {_fmt(val)} | {cat} | {pm} | {dt.strftime('%d/%m')}")
    else:
        lines.append("Nenhum gasto registrado.")
    finance_bot.send_message(chat_id, "\n".join(lines), parse_mode="Markdown")


def cmd_summary(message, finance_bot):
    chat_id = message.chat.id
    now = datetime.now()
    total_gain, total_spent = db.get_monthly_totals()
    balance = total_gain - total_spent
    lines = [f"**Resumo de {MONTH_NAMES[now.month]}/{now.year}**\n"]
    lines.append(f"**Ganhos: {_fmt(total_gain)}**")
    gain_cats, _ = db.get_monthly_summary("gain")
    for row in gain_cats:
        cat, total, count = row
        lines.append(f"  {cat}: {_fmt(total)} ({count}x)")
    lines.append("")
    lines.append(f"**Gastos: {_fmt(total_spent)}**")
    spent_cats, _ = db.get_monthly_summary("spent")
    for row in spent_cats:
        cat, total, count = row
        lines.append(f"  {cat}: {_fmt(total)} ({count}x)")
    lines.append("")
    lines.append(f"**Saldo: {_fmt(balance)}**")
    finance_bot.send_message(chat_id, "\n".join(lines), parse_mode="Markdown")
