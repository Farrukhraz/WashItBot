from telegram import ReplyKeyboardMarkup


def get_main_keyboard():
    reply_keyboard = [
        ['Статус 📊', 'Помощь 📚'],
        ['Занять машинку 🧼', 'Попросить забрать вещи 🧺']
    ]
    return ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

