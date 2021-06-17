from telegram import Update
from telegram.ext import CallbackContext

from WashItBot.main import WASHING_MACHINES_MONITORING_UTIL
from WashItBot.settings import CHOOSING, PHOTO_NOTIFY_USER, LOGGER
from WashItBot.keyboards.main_keyboards import get_main_keyboard
from WashItBot.utils.qrcode_reader_util import get_machine_number
from WashItBot.utils.notifier_util import notify_user


def main(update: Update, context: CallbackContext) -> int:
    """ Notifies user who used machine and didn't take his clothes """

    reply_text = "Кто то не забрал свои вещи вовремя? 🤦‍♀️\n\n" \
                 "Сфотаграфируй и отправь, пожалуйста, QR код машинки, в которой лежат вещи\n\n" \
                 "Либо отправь /skip чтобы попасть в главное меню\n" \
                 "/skip    /skip   /skip   /skip"
    # Как вариант, можно отправить юзеру фото инструкцию, как это сделать
    update.message.reply_text(
        reply_text,
    )
    LOGGER.debug("Trying to notify user about forgotten clothes", update)
    return PHOTO_NOTIFY_USER


def skip_notify_user(update: Update, context: CallbackContext) -> int:
    reply_text = "Ладно, похоже что забытых вещей нет 💆🏼 "
    update.message.reply_text(
        reply_text,
        reply_markup=get_main_keyboard(),
    )
    LOGGER.debug("Canceling sending notification about forgotten clothes", update)
    return CHOOSING


def process_received_photo(update: Update, context: CallbackContext) -> int:
    """ Find qr code in image. If QR code content is valid those known machine is given
     then process the request. If unknown QR code or image is given, send warning message """
    photo_file = update.message.photo[-1].get_file()
    try:
        machine_name, machine_number = get_machine_number(photo_file.file_path)
    except ValueError:
        machine_name, machine_number = None, None
    if None not in [machine_name, machine_number]:
        machine_id = f"{machine_name}:{machine_number}"
        if WASHING_MACHINES_MONITORING_UTIL.is_machine_busy(machine_id):
            reply_text = f"Страно, но {machine_name} №{machine_number} всё ещё работает.\n" \
                         "Может ты перепутал машинку?\n\n" \
                         "Попробуй отсканировать QR код нужной машинки\n" \
                         "/skip    /skip   /skip   /skip"
            update.message.reply_text(
                reply_text,
            )
            LOGGER.debug(f"Trying to notify user of the busy machine. Machine_id: {machine_id}", update)
            return PHOTO_NOTIFY_USER
        else:
            reply_text = f"То что надо! {machine_name} №{machine_number}. \n\n" \
                         f"Если человечек, который не забрал вещи использовал бота, " \
                         f"то он получит оповещение"
        update.message.reply_text(
            reply_text,
            reply_markup=get_main_keyboard(),
        )
        LOGGER.debug("Photo of QR code for sending notification about forgotten clothes processed", update)
        __notify_user(machine_id)
        return CHOOSING
    else:
        reply_text = "Не могу найти нужный мне QR код на изображении. " \
                     "Пожалуйста, попробуй сфотаграфировать его ещё раз\n\n" \
                     "Либо отправь /skip если передумал\n" \
                     "/skip    /skip   /skip   /skip"
        update.message.reply_text(
            reply_text,
        )
        return PHOTO_NOTIFY_USER


def __notify_user(machine_id: str) -> None:
    LOGGER.debug("Trying to notify user of forgotten clothes")
    machine = WASHING_MACHINES_MONITORING_UTIL.get_machine(machine_id)
    if machine:
        LOGGER.debug(f"Machine with id={machine_id} was found. Trying to send a notification")
        notify_user(machine)
    else:
        LOGGER.debug(f"Machine with id={machine_id} wasn't found. Notification isn't sent")

























