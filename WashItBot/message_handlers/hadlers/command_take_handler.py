from telegram import Update
from telegram.ext import CallbackContext

from WashItBot.settings import CHOOSING, PHOTO_TAKE_MACHINE, TIME_TAKE_MACHINE
from WashItBot.keyboards.main_keyboards import get_main_keyboard
from WashItBot.utils.qrcode_reader_util import get_machine_number


def main(update: Update, context: CallbackContext) -> int:
    reply_text = "Хорошо, давай займём машинку.\n" \
                 "Сфотаграфируй и отправь, пожалуйста, QR код машинки, в которую ты хочешь положить вещи\n\n" \
                 "Либо отправь /skip если передумал\n" \
                 "/skip    /skip   /skip   /skip"
    # Как вариант, можно отправить юзеру фото инструкцию, как это сделать
    update.message.reply_text(
        reply_text,
    )
    return PHOTO_TAKE_MACHINE


def skip_take_machine(update: Update, context: CallbackContext) -> int:
    reply_text = "Передумал стираться? Хм, ну ладно, как нибудь в другой раз =)"
    update.message.reply_text(
        reply_text,
        reply_markup=get_main_keyboard(),
    )
    return CHOOSING


def process_received_photo(update: Update, context: CallbackContext) -> int:
    """ Find qr code in image. If QR code content is valid those known machine is given
     then process the request. If unknown QR code or image is given, send warning message """
    # user = update.message.from_user   # for log
    photo_file = update.message.photo[-1].get_file()
    try:
        machine_name, machine_number = get_machine_number(photo_file.file_path)
    except ValueError:
        machine_name, machine_number = None, None
    if None not in [machine_name, machine_number]:
        reply_text = f"Ага, вижу. {machine_name} №{machine_number}. \n\n" \
                     f"Чтобы занять её, нужно ещё указать время, " \
                     "которое осталось до конца стирки"
        update.message.reply_text(
            reply_text,
        )
        return TIME_TAKE_MACHINE
    else:
        reply_text = "Не могу найти нужный мне QR код на изображении. " \
                     "Пожалуйста, попробуй сфотаграфировать его ещё раз\n\n" \
                     "Либо отправь /skip если передумал\n" \
                     "/skip    /skip   /skip   /skip"
        update.message.reply_text(
            reply_text,
        )
        return PHOTO_TAKE_MACHINE


def process_received_time(update: Update, context: CallbackContext) -> int:
    """ Process time that user send """
    text = update.message.text
    try:
        processed_time = int(text)
        if processed_time < 1 or processed_time > 60:
            raise ValueError
    except ValueError:
        processed_time = None
    if processed_time:
        reply_text = f"Супер, время вижу.\nНу что? Машинка твоя на ближайшие {processed_time} минут.\n\n" \
                     "Я отправлю тебе оповещение за 5 минут до конца стирки =)"
        update.message.reply_text(
            reply_text,
            reply_markup=get_main_keyboard(),
        )

        # ToDo create event for this machine
        # ToDo create reminder for this user

        return CHOOSING
    else:
        reply_text = "Не могу разобрать твоё сообщение =(\n" \
                     "Отправь, пожалуйста, число в диапазоне от 2 до 60. " \
                     "Число должно обозначать то, сколько времени оставлось до конца стирки.\n" \
                     "Например: \n45 или 12\n\n" \
                     "Либо отправь /skip если передумал\n" \
                     "/skip    /skip   /skip   /skip"
        update.message.reply_text(
            reply_text,
        )
        return TIME_TAKE_MACHINE
