from telegram import Update
from telegram.ext import CallbackContext

from WashItBot.settings import CHOOSING, LOGGER
from WashItBot.keyboards.main_keyboards import get_main_keyboard


START_MESSAGE = """
Привет 🙋🏽
Рад что ты решил воспользоваться моей помощью 

Чтобы узать что я умею, нажми на кнопку "Помощь 📚"

Удачной стирки =)
"""


def main(update: Update, context: CallbackContext) -> int:
    """Starts the conversation."""

    update.message.reply_text(
        text=START_MESSAGE,
        reply_markup=get_main_keyboard(),
    )
    LOGGER.debug("Starting the bot", update)
    return CHOOSING
