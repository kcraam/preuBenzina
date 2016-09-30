#!/usr/bin/python
# -*- coding: utf-8 -*-
import telegram

__author__ = "Kcraam"
__date__ = "30/9/16"

from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
from telegram.ext import CommandHandler

updater = Updater(token='')
dispatcher = updater.dispatcher

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)



updater.start_polling()

def start(bot, update):
        bot.sendMessage(chat_id=update.message.chat_id, text="Hola, soc un bot, parlam!")


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

def echo(bot, update):
        bot.sendMessage(chat_id=update.message.chat_id, text=update.message.text)


echo_handler = MessageHandler([Filters.text], echo)
dispatcher.add_handler(echo_handler)

def caps(bot, update, args):
        text_caps = ' '.join(args).upper()
        bot.sendMessage(chat_id=update.message.chat_id, text=text_caps)

caps_handler = CommandHandler('caps', caps, pass_args=True)
dispatcher.add_handler(caps_handler)

def google(bot, update, args):
        bot.sendMessage(chat_id=update.message.chat_id, text = "*bold* _italic_ [link](http://google.com).", parse_mode = telegram.ParseMode.MARKDOWN)


google_handler = CommandHandler('google', google, pass_args=True)
dispatcher.add_handler(google_handler)

def gasoil(bot, update, args):
        location_keyboard = telegram.KeyboardButton(text="Posicio", request_location=True)
        contact_keyboard = telegram.KeyboardButton(text="Contacte", request_contact=True)
        custom_keyboard = [[location_keyboard, contact_keyboard]]
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.sendMessage(chat_id=update.message.chat_id, text="Digue'm on ets", reply_markup=reply_markup)

gasoil_handler = CommandHandler('gasoil', gasoil, pass_args=True)
dispatcher.add_handler(gasoil_handler)

def unknown(bot, update):
        bot.sendMessage(chat_id=update.message.chat_id, text="Ho sento, no t'he entes.")

unknown_handler = MessageHandler([Filters.command], unknown)
dispatcher.add_handler(unknown_handler)


updater.idle()

# https://github.com/python-telegram-bot/python-telegram-bot/wiki/Code-snippets