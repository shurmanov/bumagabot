from uuid import uuid4

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardButton,
                      InlineKeyboardMarkup)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler, CallbackQueryHandler)

import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

LANGUAGE, PERIOD, DAY, TIME, ROLL_NUMBER, SEND_LOC, DOM, KVARTIRA, SEND_CONT, BYE = range(10)

my_user = dict()


def start(bot, update):
    subscribe_button = KeyboardButton(text='Obuna bo\'lish/ Подписаться')
    keyboard = [[subscribe_button]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    bot.send_message(chat_id=update.message.chat_id, text='Yangicha hayotni istaysizmi?! Unda tugmani bosing!'
                                                          '\n Хотите новую жизнь?! Тогда жмите сюда!', reply_markup=reply_markup)

    return LANGUAGE


def language(bot, update):
    reply_keyboard = [['O\'zbekcha', 'Русский']]

    update.message.reply_text(
        'Tilni tanlang / Выберите язык: ',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=True))

    return PERIOD


def period(bot, update):
    switcher = {
        'O\'zbekcha': ['1 oy', '3 oy', '6 oy', 'Obuna davrini tanlang'],
        'Русский': ['1 месяца', '3 месяца', '6 месяцев', 'Выберите период подписки']
    }
    my_user[update.message.from_user.id] = update.message.text

    lang = my_user[update.message.from_user.id]
    update.message.reply_text(
        switcher.get(lang)[3],
        reply_markup=ReplyKeyboardMarkup([switcher.get(lang)[:3]], resize_keyboard=True, one_time_keyboard=True))
    return DAY


def day(bot, update):
    switcher = {
        'O\'zbekcha': ['Dush-Juma', 'Shanba', 'Yakshanba', 'Yetkazish kunini tanlang'],
        'Русский': ['Пон-Пят', 'Суббота', 'Воскр', 'Выберите день недели доставки']
    }
    lang = my_user[update.message.from_user.id]
    update.message.reply_text(
        switcher.get(lang)[3],
        reply_markup=ReplyKeyboardMarkup([switcher.get(lang)[:3]], resize_keyboard=True, one_time_keyboard=True))
    return TIME


def which_time(bot, update):
    switcher = {
        'O\'zbekcha': ['Ertalab', 'Tushlikda', 'Kechqurun', 'Kun qismini tanlang'],
        'Русский': ['Утром', 'Обед', 'Вечером', 'Выберите часть дня']
    }

    lang = my_user[update.message.from_user.id]
    update.message.reply_text(
        switcher.get(lang)[3],
        reply_markup=ReplyKeyboardMarkup([switcher.get(lang)[:3]], resize_keyboard=True, one_time_keyboard=True))
    return ROLL_NUMBER

def roll_number(bot, update):
    switcher = {
        'O\'zbekcha': ['4', '6', '12', 'Rulonlar soni:'],
        'Русский': ['4', '6', '12', 'Количество рулонов:']
    }

    lang = my_user[update.message.from_user.id]
    update.message.reply_text(
        switcher.get(lang)[3],
        reply_markup=ReplyKeyboardMarkup([switcher.get(lang)[:3]], resize_keyboard=True, one_time_keyboard=True))
    return SEND_LOC


def send_loc(bot, update):
    switcher = {
        'O\'zbekcha': ['Ulashish', 'Joylashuvingiz bizga muhim:'],
        'Русский': ['Дать локацию', 'Нам важно Ваше Местоположение:']
    }
    lang = my_user[update.message.from_user.id]

    subscribe_button = KeyboardButton(text=switcher.get(lang)[0], request_location=True)
    keyboard = [[subscribe_button]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    bot.send_message(chat_id=update.message.chat_id, text=switcher.get(lang)[1], reply_markup=reply_markup)

    return DOM


def dom(bot, update):
    switcher = {
        'O\'zbekcha': ['Uy:', 'Nechinchi uy(raqamlar bilan): '],
        'Русский': ['Дом:', 'Какой дом(цифрами): ']
    }
    lang = my_user[update.message.from_user.id]
    update.message.reply_text(
        switcher.get(lang)[1])
    return KVARTIRA

def kvartira(bot, update):
    switcher = {
        'O\'zbekcha': ['Xonadon:', 'Nechinchi xonadon(aniqlik uchun): '],
        'Русский': ['Квартира:', 'Какая квартира(для точности): ']
    }
    lang = my_user[update.message.from_user.id]
    update.message.reply_text(
        switcher.get(lang)[1])

    return SEND_CONT


def send_contact(bot, update):
    switcher = {
        'O\'zbekcha': ['Tel.raqam ulashish', 'Siz bilan aloqa biz uchun muhim:'],
        'Русский': ['Дать тел.номер', 'Нам нужен ваш контакт:']
    }
    lang = my_user[update.message.from_user.id]

    subscribe_button = KeyboardButton(text=switcher.get(lang)[0], request_contact=True)
    keyboard = [[subscribe_button]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    bot.send_message(chat_id=update.message.chat_id, text=switcher.get(lang)[1], reply_markup=reply_markup)

    return BYE

def bye(bot, update):
    switcher = {
        'O\'zbekcha': ['Barcha ma\'lumotalaringiz uchun rahmat! \n EasyGo inc.'],
        'Русский': ['Спасибо за терпение!\n EasyGo inc.']
    }

    lang = my_user[update.message.from_user.id]
    update.message.reply_text(switcher.get(lang)[0])

    return SEND_CONT


def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("883849576:AAEvVttHB9ZoXh-XjsOQmalXqrvLkpcIyi0")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            LANGUAGE: [MessageHandler(Filters.all, language)],

            PERIOD: [MessageHandler(Filters.all, period)],

            DAY: [MessageHandler(Filters.all, day)],

            TIME: [MessageHandler(Filters.all, which_time)],

            ROLL_NUMBER: [MessageHandler(Filters.all, roll_number)],

            SEND_LOC: [MessageHandler(Filters.all, send_loc)],

            DOM: [MessageHandler(Filters.all, dom)],

            KVARTIRA: [MessageHandler(Filters.all, kvartira)],

            SEND_CONT: [MessageHandler(Filters.all, send_contact)],

            BYE: [MessageHandler(Filters.all, bye)],
        },

        fallbacks=[CommandHandler('cancel', cancel)],
        allow_reentry=True
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    #updater.start_polling()
    updater.start_webhook()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
