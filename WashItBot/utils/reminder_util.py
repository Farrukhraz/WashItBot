from threading import Timer


def __remind_user(user_id: str) -> None:
    pass


def remind_user(time: int, user_id: str, *args, **kwargs) -> Timer:
    """

    :param time: Time is secs
    :param args:
    :param kwargs:
    """
    return Timer(time, function=__remind_user, args=(user_id, ))


def cancel_reminder(reminder: Timer) -> None:
    """ Cancel reminder """
    reminder.cancel()

