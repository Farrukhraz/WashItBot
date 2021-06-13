from telegram import Update
from telegram.ext import CallbackContext

from WashItBot.settings import CHOOSING
from WashItBot.keyboards.main_keyboards import get_main_keyboard

from WashItBot.utils.reminder_util import remind_me


def main(update: Update, context: CallbackContext) -> int:
    """ Notifies user who used machine and didn't take his clothes """

    # find out which machine is scanned
    # check that machine is busy or not
    # if it isn't busy - let the user to take it - else - say current user that machine is still working

    update.message.reply_text(
        reply_text,
        reply_markup=get_main_keyboard(),
    )
    return CHOOSING
