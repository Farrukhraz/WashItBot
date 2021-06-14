from telegram import Update
from telegram.ext import CallbackContext

from WashItBot.settings import CHOOSING, PHOTO_TAKE_MACHINE, TIME_TAKE_MACHINE
from WashItBot.keyboards.main_keyboards import get_main_keyboard

from WashItBot.utils.reminder_util import ReminderUtil


def main(update: Update, context: CallbackContext) -> int:
    reply_text = "Хорошо, давай займём машинку.\n" \
                 "Сфотаграфируй и отправль пожалуйста QR код машинки, в которую ты хочешь положить вещи\n\n" \
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


def process_received_photo(update: Update, context: CallbackContext, image: str) -> int:
    """ Find qr code in image. If QR code content is valid those known machine is given
     then process the request. If unknown QR code or image is given, send warning message """
    # process...
    # process...
    processed_photo = ''
    if processed_photo:
        reply_text = "Ага, вижу. Машинка № {}. Чтобы занять её, нужно ещё указать время, " \
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


def process_received_time(update: Update, context: CallbackContext, time: str) -> int:
    """ Process time that user send """
    processed_time = ''
    if processed_time:
        reply_text = "Супер, время вижу.\nНу что? Машинка твоя на ближайшие {} минут.\n" \
                     "Я отправлю тебе оповещение за 5 минут до конца стирки =)"
        update.message.reply_text(
            reply_text,
            reply_markup=get_main_keyboard(),
        )
        return CHOOSING
    else:
        reply_text = "Не могу разобрать твоё сообщение =(\n" \
                     "Отправь, пожалуйста, число. Указывающее на то, сколько времени оставлось до конца стирки.\n" \
                     "Например: \n45 или 12\n\n" \
                     "Либо отправь /skip если передумал\n" \
                     "/skip    /skip   /skip   /skip"
        update.message.reply_text(
            reply_text,
        )
        return TIME_TAKE_MACHINE
