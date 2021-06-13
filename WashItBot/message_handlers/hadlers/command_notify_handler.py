from telegram import Update
from telegram.ext import CallbackContext

from WashItBot.settings import CHOOSING
from WashItBot.keyboards.main_keyboards import get_main_keyboard

from WashItBot.utils.notifier_util import notify_user, check_user


def main(update: Update, context: CallbackContext) -> int:
    """ Notifies user who used machine and didn't take his clothes """

    # find out which machine is scanned
    # check that machine is busy or not
    # if it isn't busy - try to notify last used user - else - say current user that machine is still working

    if check_user():
        notify_user()
        reply_text = "Пользователь оповещён. Скоро он заберёт свои вещи =)"
    else:
        reply_text = "Не получается найти чьи это вещи. Видимо пользователь не воспользовался ботом =("

    update.message.reply_text(
        reply_text,
        reply_markup=get_main_keyboard(),
    )
    return CHOOSING
