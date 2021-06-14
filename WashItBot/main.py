import os

from telegram.ext import (
    Updater,
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackQueryHandler,
)

from WashItBot.settings import (
    TOKEN,
    CHOOSING,
    PHOTO_NOTIFY_USER,
    PHOTO_TAKE_MACHINE,
    TIME_TAKE_MACHINE,
)
from WashItBot.message_handlers.hadlers import (
    command_help_handler,
    command_notify_handler,
    command_start_handler,
    command_status_handler,
    command_take_handler,
    delete_unknown_command,
)


def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', command_start_handler.main),
        ],
        states={
            CHOOSING: [
                CommandHandler('help', command_help_handler.main),
                MessageHandler(
                    Filters.regex('^take machine'), command_take_handler.main
                ),
                MessageHandler(
                    Filters.regex('^notify me later'), command_notify_handler.main
                ),
                MessageHandler(
                    Filters.regex('^show status'), command_status_handler.main
                ),
                MessageHandler(
                    Filters.regex('^help me'), command_help_handler.main
                ),
            ],
            PHOTO_TAKE_MACHINE: [
                MessageHandler(Filters.photo, command_take_handler.process_received_photo),
                CommandHandler('skip', command_take_handler.skip_take_machine),
            ],
            TIME_TAKE_MACHINE: [
                MessageHandler(Filters.regex(r'^\d\d'), command_take_handler.process_received_time),
                CommandHandler('skip', command_take_handler.skip_take_machine),
            ],
            PHOTO_NOTIFY_USER: [
                MessageHandler(Filters.photo, command_notify_handler.photo)
            ],
        },
        fallbacks=[
            # Restart main menu
            CommandHandler('start', command_start_handler.main),
            # If user sends text message rather than pressing menu button, delete this message
            MessageHandler(
                Filters.text & (~Filters.command), delete_unknown_command
            ),
        ],
    )
    dispatcher.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


