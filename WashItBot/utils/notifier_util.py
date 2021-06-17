# This util is used to notify last user to take his clothes
from time import time

from telegram import Update

from WashItBot.settings import CHOOSING, LOGGER
from WashItBot.keyboards.main_keyboards import get_main_keyboard
from WashItBot.utils.monitoring_util import WashingProcess
from WashItBot.utils.logging_util import get_user_info


def notify_user(machine: WashingProcess) -> None:
    """
    Notify user to take his forgotten clothes
    Notifications can be send not more than once a minute
    """
    update: Update = machine.user_update
    if _is_notification_allowed(machine):
        name, number = machine.machine_id.split(':')
        reply_text = f"{name} №{number} закончила работу.\n" \
                     f"И кто там внизу просит, чтобы ты забрал свои вещи"
        update.message.reply_text(
            text=reply_text,
            reply_markup=get_main_keyboard(),
        )
        machine.last_notification_time = time()
        LOGGER.debug(f"Notification about forgotten clothes is sent to '{get_user_info(update)}'")
        return CHOOSING
    LOGGER.debug(f"Notification about forgotten clothes is not allowed to '{get_user_info(update)}'")


def _is_notification_allowed(machine: WashingProcess) -> bool:
    is_allowed = False
    if (time() - machine.end_time) > (60 * 60):
        # if machine finished more than 1 hours ago
        return is_allowed
    if (time() - machine.last_notification_time) < 60:
        # if last notification was send less than a minute ago
        return is_allowed
    return True


