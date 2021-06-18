from telegram import Update
from telegram.ext import CallbackContext

from WashItBot.main import WASHING_MACHINES_MONITORING_UTIL
from WashItBot.settings import CHOOSING, PHOTO_TAKE_MACHINE, TIME_TAKE_MACHINE, LOGGER
from WashItBot.keyboards.main_keyboards import get_main_keyboard
from WashItBot.utils.qrcode_reader_util import get_machine_number
from WashItBot.utils.reminder_util import create_reminder


def main(update: Update, context: CallbackContext) -> int:
    reply_text = "Хорошо, давай займём машинку 🧼\n\n" \
                 "Сфотаграфируй и отправь, пожалуйста, QR код машинки, в которую ты хочешь положить вещи\n\n" \
                 "Либо отправь /skip если передумал\n" \
                 "/skip    /skip   /skip   /skip"
    # Как вариант, можно отправить юзеру фото инструкцию, как это сделать
    update.message.reply_text(
        reply_text,
    )
    LOGGER.debug("Trying to take the machine", update)
    return PHOTO_TAKE_MACHINE


def skip_take_machine(update: Update, context: CallbackContext) -> int:
    reply_text = "Передумал стираться? Хм, ну ладно, как нибудь в другой раз 💁‍♀️"
    if context.user_data.get('machine_id'):
        del context.user_data['machine_id']
    update.message.reply_text(
        reply_text,
        reply_markup=get_main_keyboard(),
    )
    LOGGER.debug("Skipping taking the machine", update)
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
        machine_id = f"{machine_name}:{machine_number}"
        context.user_data['machine_id'] = machine_id
        if WASHING_MACHINES_MONITORING_UTIL.is_machine_busy(machine_id):
            reply_text = 'Так, так. Похоже что машинка уже занята. \n' \
                         'Давай попробуем другую машинку?\n\n' \
                         'Для того чтобы занять другую, отправь мне QR код машинки\n\n' \
                         "Если передумал занимать машинку отправь\n" \
                         "/skip    /skip   /skip   /skip"
            update.message.reply_text(
                reply_text,
            )
            LOGGER.debug(f"Trying to take the busy machine. Machine_id: {machine_id}", update)
            return PHOTO_TAKE_MACHINE
        else:
            reply_text = f"Ага, вижу. {machine_name} №{machine_number}. \n\n" \
                         f"Чтобы занять её, нужно указать время стирки (в минутах)\n" \
                         f"Введи число от 1 до 60 и машинка будет твоей\n\n" \
                         "Либо отправь /skip если передумал\n" \
                         "/skip    /skip   /skip   /skip"
            update.message.reply_text(
                reply_text,
            )
            LOGGER.debug(f"Machine is being taken. Machine_id: {machine_id}", update)
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
    processed_time = __process_time(update.message.text)
    if processed_time:
        reply_text, is_machine_taken = __take_machine(update, context, processed_time)
        if is_machine_taken:
            __create_reminder(processed_time, update)
        update.message.reply_text(
            reply_text,
            reply_markup=get_main_keyboard(),
        )
        return CHOOSING
    else:
        reply_text = "Не могу разобрать твоё сообщение =(\n" \
                     "Отправь, пожалуйста, число в диапазоне от 1 до 60. " \
                     "Число должно обозначать то, сколько времени оставлось до конца стирки.\n" \
                     "Например: \n45 или 12\n\n" \
                     "Либо отправь /skip если передумал\n" \
                     "/skip    /skip   /skip   /skip"
        update.message.reply_text(
            reply_text,
        )
        return TIME_TAKE_MACHINE


def __process_time(text: str) -> int:
    try:
        _time = int(text)
        if _time < 1 or _time > 60:
            raise ValueError
        processed_time = _time * 60
    except ValueError:
        processed_time = None
    return processed_time


def __take_machine(update: Update, context: CallbackContext, _time) -> (str, bool):
    machine_id = context.user_data.get('machine_id')
    machine_taken = True
    if not machine_id:
        LOGGER.error("Trying to process the time but id of the machine is not recognized", update)
        reply_text = f"Что то пошло не так =( \n\n Пожалуйста, останови меня через кнопку stop и перезапусти"
        machine_taken = False
    else:
        LOGGER.debug(f"Machine was taken for {_time} seconds", update)
        WASHING_MACHINES_MONITORING_UTIL.take_machine(user_update=update, user_context=context,
                                                      machine_id=machine_id, _time=_time)
        reply_text = f"Супер, время вижу.\nНу что? Машинка твоя на ближайшие {_time//60} мин."
        if _time >= 5 * 60:
            reply_text = f"{reply_text}\n\nЯ отправлю тебе оповещение примерно за 5 минут до конца твоей стирки =)"
    return reply_text, machine_taken


def __create_reminder(_time, update: Update) -> None:
    if _time < 5 * 60:
        LOGGER.debug(f"Reminder wasn't created because the time before machine finishes less than 5 minutes", update)
        return
    remind_time = int(_time - 4.5 * 60)
    LOGGER.debug(f"Creating reminder for {remind_time} seconds", update)
    create_reminder(remind_time, update)
