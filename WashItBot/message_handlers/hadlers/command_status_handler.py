from telegram import Update
from telegram.ext import CallbackContext

from WashItBot.settings import CHOOSING
from WashItBot.keyboards.main_keyboards import get_main_keyboard

# from WashItBot.utils.status_util import get_current_status
#

def main(update: Update, context: CallbackContext) -> int:
    """ Sends machines current status """

    # update.message.reply_text(
    #     get_current_status(),
    #     reply_markup=get_main_keyboard(),
    # )
    return CHOOSING
