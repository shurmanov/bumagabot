

"""
1 - start ngrok
2 - setWebhook
THAT's All
https://api.telegram.org/bot883849576:AAEvVttHB9ZoXh-XjsOQmalXqrvLkpcIyi0/setwebhook?url=https://895c81fe.ngrok.io

TOKEN
727157893:AAGvCVG-7y6MIsi7sc3W_kQ0Cv-Sa36gE8Q

"""

import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def controller(state, ):
    switcher = {

    }
    district = ['Yunusobod', 'Chilonzor', 'Mirzo Ulugbek', 'Mirobod']
    kvartal = [range(1, 19), range(1, 19), range(1, 19)]
    dom = []
    subscription_options = ['2 months', '4 months', '6 months']
    day_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    time_of_day = ['Morning', 'Afternoon', 'Evening', 'Night']
    num_of_rolls = []


def district_menu(bot, update, lang):

    switcher = {
        '0': ['Yunusobod', 'Chilonzor', 'Mirzo Ulugbek', 'Mirobod'],
        '1': ['Юнусабадский', 'Чиланзарский', 'Мирзо Улугбекский', 'Мирабадский']
    }
    lang_switcher = {
        '0': 'Tumanni tanlang',
        '1': 'Выберите район'
    }

    keyboard = [[]]

    for count, district in enumerate(switcher[lang]):
        k = InlineKeyboardButton(district, callback_data=count+2)
        keyboard[0].append(k)

    reply_markup = InlineKeyboardMarkup(keyboard)

    bot.send_message(chat_id=update.message.chat_id, text=lang_switcher[lang], reply_markup=reply_markup)


def query_function_mapper(bot, update, lang):
    # switcher = [district_menu, kvartal_menu,
    #             dom_menu, period_menu,
    #             day_menu, time_menu,
    #             num_of_rolls_menu, contact_menu]
    switcher = [district_menu, ]

    return switcher[int(update.callback_query.data) - 1]

def start(bot, update):


    #update.message.reply_text('Please choose:', reply_markup=reply_markup)
    # kb = KeyboardButton("Hey hi!!!")
    # update.message.reply_text(kb)
    subscribe_button = KeyboardButton(text="/subscribe")
    keyboard = [[subscribe_button]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    bot.send_message(chat_id=update.message.chat_id, text='Press on the subscribe button!!!', reply_markup=reply_markup)


def subscribe(bot, update):
    keyboard = [[InlineKeyboardButton("O'zbekcha", callback_data='1'),
                 InlineKeyboardButton("Русский", callback_data='2')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    bot.send_message(chat_id=update.message.chat_id, text='Choose language:', reply_markup=reply_markup)


def button(bot, update):
    query = update.callback_query
    if query.data == '1':
        query_function_mapper(bot, update)(bot, update, '0')
    else:
        query_function_mapper(bot, update)(bot, update, '1')

    # bot.edit_message_text(text="Selected option: {}".format(query.data),
    #                       chat_id=query.message.chat_id,
    #                       message_id=query.message.message_id)


def help(bot, update):
    update.message.reply_text("Use /start to test this bot.")


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater("727157893:AAGvCVG-7y6MIsi7sc3W_kQ0Cv-Sa36gE8Q")

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(CommandHandler('subscribe', subscribe))
    updater.dispatcher.add_handler(CommandHandler('help', help))
    updater.dispatcher.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()