import logging
import os
import ruuvitag_sensor.log
from credentials import credentials
from ruuvitag_sensor.ruuvi import RuuviTagSensor
from telegram.ext import Updater, CommandHandler
from firebase import DataBase


def get_data():
    ruuvitag_sensor.log.enable_console()
    data = RuuviTagSensor.find_ruuvitags()
    return data


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


def weather(update, context):
    # context.bot.send_message(chat_id=update.effective_chat.id, text=get_data())
    context.bot.send_message(chat_id=update.effective_chat.id, text='This command shows the latest weather data from'
                                                                    ' the Firebase database')
    context.bot.send_message(chat_id=update.effective_chat.id, text='From {rid}, Time: {date}, Temperature: {temp}°C,'
                                                                    'Humidity: {hum}, Air pressure: {ap}'
                             .format(rid=rid, date=date, temp=temp, hum=hum, ap=ap))


def air_pressure(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Air pressure from {rid} at {date}: {hum}'
                             .format(rid=rid, date=date, hum=hum))


def humidity(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Humidity from {rid} at {date}: {hum}'
                             .format(rid=rid, date=date, hum=hum))


def temperature(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Temperature from {rid} at {date}: {temp}°C'.format(rid=rid, date=date, temp=temp))


def weather_graph(update, context):
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('graph.png', 'rb'))
    context.bot.send_message(chat_id=update.effective_chat.id, text='Weather graph from last 7 days')


if __name__ == '__main__':
    db = DataBase()
    ap, hum, rid, temp, date = db.get_latest()
    creds = credentials.require(['api'])
    updater = Updater(token=creds.api)

    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)  # Start
    dispatcher.add_handler(start_handler)
    weather_handler = CommandHandler('weather', weather)  # Weather
    dispatcher.add_handler(weather_handler)
    pressure_handler = CommandHandler('air_pressure', air_pressure)  # Air pressure
    dispatcher.add_handler(pressure_handler)
    hum_handler = CommandHandler('humidity', humidity)  # Humidity
    dispatcher.add_handler(hum_handler)
    temp_handler = CommandHandler('temperature', temperature)  # Humidity
    dispatcher.add_handler(temp_handler)
    graph_handler = CommandHandler('weather_graph', weather_graph)  # Weather graph
    dispatcher.add_handler(graph_handler)

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    updater.start_polling()
