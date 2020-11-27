import logging
import os
import ruuvitag_sensor.log
from credentials import credentials
from ruuvitag_sensor.ruuvi import RuuviTagSensor
from telegram.ext import Updater, CommandHandler


def get_data():
    ruuvitag_sensor.log.enable_console()
    data = RuuviTagSensor.find_ruuvitags()
    return data


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


def weather(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=get_data())


def otit(update, context):
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('otit_logo_fill.jpg', 'rb'))


if __name__ == '__main__':
    creds = credentials.require(['api'])
    updater = Updater(token=creds.api)

    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    weather_handler = CommandHandler('weather', weather)
    dispatcher.add_handler(weather_handler)

    otit_handler = CommandHandler('otit', otit)
    dispatcher.add_handler(otit_handler)

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    updater.start_polling()
