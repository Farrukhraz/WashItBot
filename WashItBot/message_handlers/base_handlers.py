from telegram import Update
from telegram.ext import CallbackContext

from WashItBot.settings import CHOOSING
from WashItBot.keyboards.main_keyboards import get_main_keyboard


def delete_unknown_command(update: Update, context: CallbackContext):
    reply_text = "Извини, но я не понимаю тебя 🙅🏽‍♂️\n\nВыбери подходящую команду из меню 👇🏼"
    update.message.reply_text(
        text=reply_text,
        reply_markup=get_main_keyboard(),
    )
    return CHOOSING

