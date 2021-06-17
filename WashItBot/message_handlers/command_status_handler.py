from telegram import Update
from telegram.ext import CallbackContext

from WashItBot.main import WASHING_MACHINES_MONITORING_UTIL
from WashItBot.settings import CHOOSING, LOGGER
from WashItBot.keyboards.main_keyboards import get_main_keyboard


def main(update: Update, context: CallbackContext) -> int:
    """ Sends machines current status """
    update.message.reply_text(
        get_current_status(),
        reply_markup=get_main_keyboard(),
    )
    LOGGER.debug("Asking for machines status", update)
    return CHOOSING


def get_current_status() -> str:
    status: list = WASHING_MACHINES_MONITORING_UTIL.get_status()
    return str(status)
