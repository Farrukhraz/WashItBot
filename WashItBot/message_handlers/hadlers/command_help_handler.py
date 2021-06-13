from telegram import Update
from telegram.ext import CallbackContext

from WashItBot.settings import CHOOSING
from WashItBot.keyboards.main_keyboards import get_main_keyboard


def main(update: Update, context: CallbackContext) -> int:
    """ Sends help message """

    update.message.reply_text(
        'Сообщение с инструкциями',
        reply_markup=get_main_keyboard(),
    )
    return CHOOSING
