import logging
import os
import ruuvitag_sensor.log
#from credentials import credentials
from ruuvitag_sensor.ruuvi import RuuviTagSensor
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext
from firebase import DataBase
from telegram import ReplyKeyboardMarkup

data = {'timescale':""}
TIMES = 1

def get_data():
    ruuvitag_sensor.log.enable_console()
    data = RuuviTagSensor.find_ruuvitags()
    return data


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a weather bot. Hi!")


def weather(update, context):
    ap, hum, rid, temp, date = db.get_latest()
    # context.bot.send_message(chat_id=update.effective_chat.id, text=get_data())
    context.bot.send_message(chat_id=update.effective_chat.id, text='This command shows the latest weather data from'
                                                                    ' the Firebase database')
    context.bot.send_message(chat_id=update.effective_chat.id, text='From {rid}, Time: {date}, Temperature: {temp}°C,'
                                                                    'Humidity: {hum}, Air pressure: {ap}'
                             .format(rid=rid, date=date, temp=temp, hum=hum, ap=ap))

def air_pressure(update, context):
    ap, hum, rid, temp, date = db.get_latest()
    context.bot.send_message(chat_id=update.effective_chat.id, text='Air pressure from {rid} at {date}: {hum}'
                             .format(rid=rid, date=date, hum=hum))


def humidity(update, context):
    ap, hum, rid, temp, date = db.get_latest()
    context.bot.send_message(chat_id=update.effective_chat.id, text='Humidity from {rid} at {date}: {hum}'
                             .format(rid=rid, date=date, hum=hum))

def temperature(update, context):
    global data
    data = {"timescale": ""}
    reply = [["latest from fridge", "hour from fridge", "latest from inside", "hour from inside"]] #week and year are too long 
    update.message.reply_text("Hi! From what timeline and from where would you like to see the temperature?", reply_markup=ReplyKeyboardMarkup(reply, one_time_keyboard=False),)
    return TIMES
    
def temperature2(update, context):
    data["timescale"] = update.message.text
     
    #ap, hum, rid, temp, date = db.get_latest()
    ap, hum, temp, time = db.get_latest( data["timescale"])
    textt = ""
    i=0
    #Make a list of the data
    for a in ap:
        textt += 'Temperature from {time}: {temp}°C'.format(time=time[i], temp=temp[i])
        textt += "\n"
        i = i+1
    context.bot.send_message(chat_id=update.effective_chat.id, text=textt)

def weather_graph(update, context):
    #ap, hum, rid, temp, date = db.get_latest()
    ap, hum, temp, time = db.get_latest()
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('graph.png', 'rb'))
    context.bot.send_message(chat_id=update.effective_chat.id, text='Weather graph from last 7 days')

def cancel(update, context):

    update.message.reply_text('canceled')

    # end of conversation
    return ConversationHandler.END

if __name__ == '__main__':
    db = DataBase()
    #creds = credentials.require(['api'])
    #pdater = Updater(token=creds.api)
    updater = Updater(token="1459062128:AAHekgpf4yzZQ3qyxTBLrTUo5FHo9e0UYZk")
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)  # Start
    dispatcher.add_handler(start_handler)
    weather_handler = CommandHandler('weather', weather)  # Weather
    dispatcher.add_handler(weather_handler)
    pressure_handler = CommandHandler('air_pressure', air_pressure)  # Air pressure
    dispatcher.add_handler(pressure_handler)
    hum_handler = CommandHandler('humidity', humidity)  # Humidity
    dispatcher.add_handler(hum_handler)
    #temp_handler = CommandHandler('temperature', temperature)  # 
    #dispatcher.add_handler(temp_handler)
    graph_handler = CommandHandler('weather_graph', weather_graph)  # Weather graph
    dispatcher.add_handler(graph_handler)

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    #This allows the user to "communicate" with the bot. Allows the choosing of data point
    #The temperature2 in MessageHandler means where do we go after temperature function has finished and returned TIMES
    conversation_handler = ConversationHandlerd
        entry_points=[CommandHandler('temperature', temperature)],
        states={
            TIMES: [
                MessageHandler(Filters.text, temperature2)
            ],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
        )                

    dispatcher.add_handler(conversation_handler)
    
    
    
    updater.start_polling()
