import json
import logging
import os

from logging.handlers import RotatingFileHandler

from telegram import Update


def get_user_info(update: Update) -> dict:
    user_all_info = dict()
    user = update.effective_user
    user_all_info['id'] = user.id
    user_all_info['username'] = user.username
    user_all_info['full_name'] = user.full_name
    return user_all_info


class Logger:

    def __init__(self, name=__name__, default_level=logging.DEBUG):
        self.logger = logging.Logger(name)
        self.name = name

        logs_path = os.path.normpath(os.path.join(os.getcwd(), 'logs'))
        os.makedirs(logs_path, exist_ok=True)

        handlers = [
            (logging.StreamHandler,
             dict(),
             logging.DEBUG),
            (RotatingFileHandler,
             dict(
                 filename=os.path.join(logs_path, "log.log"),
                 maxBytes=26214400,  # 25MB
                 backupCount=10
             ),
             logging.DEBUG)
        ]

        if not self.logger.handlers or len(self.logger.handlers) < 1:
            for handler_class, params, level in handlers:
                handler = handler_class(**params)
                handler.setFormatter(logging.Formatter(
                    f"%(asctime)s\t<%(levelname)s>\t%(message)s", "%b %d %H:%M:%S"))
                handler.setLevel(level if not default_level else default_level)
                self.logger.addHandler(handler)

    def prepare_message(self, message, user_info) -> str:
        return json.dumps(f"User info: {get_user_info(user_info) if user_info else ''}; "
                          f"Message: {message or ''}")

    def error(self, message=None, user_info: Update = None) -> None:
        message = self.prepare_message(message, user_info)
        self.logger.error(message, exc_info=True)

    def debug(self, message=None, user_info: Update = None) -> None:
        message = self.prepare_message(message, user_info)
        self.logger.debug(message)

    def info(self, message=None, user_info: Update = None) -> None:
        message = self.prepare_message(message, user_info)
        self.logger.info(message)

    def warning(self, message=None, user_info: Update = None) -> None:
        message = self.prepare_message(message, user_info)
        self.logger.warning(message)



