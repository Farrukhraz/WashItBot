from telegram import Update

from threading import Timer

from WashItBot.keyboards.main_keyboards import get_main_keyboard


def __remind_user(update: Update) -> None:
    text = "Пссс...\n\n" \
           "Твоя стирка закончится через 5 минут"
    update.message.reply_text(
        text,
        reply_markup=get_main_keyboard(),
    )


def create_reminder(_time: int, update: Update) -> Timer:
    """ Create reminder and notify user when time is up

    :param _time: int
        Time in seconds
    :param update: Update
    :return: Timer
        Timer objотправленect
    """
    timer = Timer(_time, function=__remind_user, args=(update,))
    timer.start()
    return timer


def cancel_reminder(reminder: Timer) -> None:
    """ Cancel reminder """
    reminder.cancel()

