#!/usr/bin/python
# -*- coding: utf-8 -*-

# https://github.com/python-telegram-bot/python-telegram-bot/wiki/Code-snippets

__author__ = "Kcraam"
__date__ = "30/9/16"

from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
from telegram.ext import CommandHandler

import telegram

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
logger = logging.getLogger(__name__)



def start(bot, update):
        bot.sendMessage(chat_id=update.message.chat_id, text="Hola, soc un bot, parlam!")


def echo(bot, update):
        bot.sendMessage(chat_id=update.message.chat_id, text=update.message.text)


def caps(bot, update, args):
        text_caps = ' '.join(args).upper()
        bot.sendMessage(chat_id=update.message.chat_id, text=text_caps)


def google(bot, update, args):
        bot.sendMessage(chat_id=update.message.chat_id, text = "*bold* _italic_ [link](http://google.com).", parse_mode = telegram.ParseMode.MARKDOWN)


def gasoil(bot, update, args):
        location_keyboard = telegram.KeyboardButton(text="Posicio", request_location=True)
        contact_keyboard = telegram.KeyboardButton(text="Contacte", request_contact=True)
        custom_keyboard = [[location_keyboard, contact_keyboard]]
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboardi, one_time_keyboard=True)
        bot.sendMessage(chat_id=update.message.chat_id, text="Digue'm on ets", reply_markup=reply_markup)
        #print([u.message.text for u in update.message.text])
        #reply_markup = telegram.ReplyKeyboardHide()
        bot.sendMessage(chat_id=chat_id, text="I'm back.", reply_markup=reply_markup)
        print args


def benzina(bot, update):
    location_keyboard = telegram.KeyboardButton(text="Posicio", request_location=True)
    contact_keyboard = telegram.KeyboardButton(text="Contacte", request_contact=True)
    custom_keyboard = [[location_keyboard, contact_keyboard]]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboardi, one_time_keyboard=True)
    bot.sendMessage(chat_id=update.message.chat_id, text="Digue'm on ets", reply_markup=reply_markup)
    # print([u.message.text for u in update.message.text])
    # reply_markup = telegram.ReplyKeyboardHide()
    bot.sendMessage(chat_id=chat_id, text="I'm back", reply_markup=reply_markup)
    print args

def location(bot, update):
    user_location = update.message.location
    print user_location

def unknown(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Ho sento, no t'he entes.")


def main():
    updater = Updater(token='')

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler([Filters.text], echo)
    caps_handler = CommandHandler('caps', caps, pass_args=True)
    google_handler = CommandHandler('google', google, pass_args=True)
    gasoil_handler = CommandHandler('gasoil', gasoil, pass_args=True)
    unknown_handler = MessageHandler([Filters.command], unknown)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(echo_handler)
    dispatcher.add_handler(caps_handler)
    dispatcher.add_handler(google_handler)
    dispatcher.add_handler(gasoil_handler)
    dispatcher.add_handler(unknown_handler)

    
    # Start the Bot
    updater.start_polling()

    # Block until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()

