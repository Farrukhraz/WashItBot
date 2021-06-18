import os
import logging

import sentry_sdk

from dotenv import load_dotenv
from telegram import Bot

from WashItBot.utils.logging_util import Logger


LOGGER = Logger()


# SHORTCUTS
# Main menu shortcuts
CHOOSING, PHOTO_TAKE_MACHINE, \
    TIME_TAKE_MACHINE, PHOTO_NOTIFY_USER, *_ = map(chr, range(3, 9))


BASE_DIR = os.getcwd()

media_root = os.path.join(BASE_DIR, 'WashItBot', 'media')


load_dotenv()

if os.environ.get('DEBUG'):
    TOKEN = os.environ.get('DEBUG_BOT_TOKEN')
else:
    TOKEN = os.environ.get('BOT_TOKEN')
    if not TOKEN:
        raise Exception("Bot token is not provided")

BOT = Bot(token=TOKEN)


sentry_sdk.init(
    "https://7134e826d08b4668a93396d6b7e9b491@o550904.ingest.sentry.io/5814252",

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0
)