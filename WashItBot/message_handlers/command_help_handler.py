from telegram import Update
from telegram.ext import CallbackContext

from WashItBot.settings import CHOOSING, LOGGER
from WashItBot.keyboards.main_keyboards import get_main_keyboard


HELP_MESSAGE = """
Ниже ты должен увидеть 4 кнопки 👇🏼:

"Статус 📊" - Информация о свободных машинках или занятые с оставшимся временем до конца стирки

"Помощь 📚" - Сообщение с инструкциями по работе с ботом

"Занять машинку 🧼" - Жми, если собираешься стираться. От тебя лишь потребуется отсканировать QR код и ввести оставшееся время стирки

"Попросить забрать вещи 🧺" - Отправить оповещение тому, кто забыл забрать свои вещи
"""


def main(update: Update, context: CallbackContext) -> int:
    """ Sends help message """

    update.message.reply_text(
        text=HELP_MESSAGE,
        reply_markup=get_main_keyboard(),
    )
    LOGGER.debug("Asking for help message", update)
    return CHOOSING
