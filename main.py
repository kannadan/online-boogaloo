from ruuvitag_sensor.ruuvi import RuuviTagSensor
import ruuvitag_sensor.log
from telegram.ext import Updater
from telegram.ext import CommandHandler
import logging
from random import randint

api = 

def get_data():
    ruuvitag_sensor.log.enable_console()
    data = RuuviTagSensor.find_ruuvitags()
    return data
    
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


def weather(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=get_data())
    

        
if __name__ == '__main__':
    updater = Updater(token=api, use_context=True)


    dispatcher = updater.dispatcher


    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    
    weather_handler = CommandHandler('weather', weather)
    dispatcher.add_handler(weather_handler)
    

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                         level=logging.INFO)
                         
    updater.start_polling()                     
                     


