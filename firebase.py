import firebase_admin
import time
from firebase_admin import credentials
from firebase_admin import db


class DataBase:

    def __init__(self):
        # Use the application default credentials
        self.cred = credentials.Certificate('online-boogaloo-firebase-adminsdk-7qkz5-8db06a938a.json')
        firebase_admin.initialize_app(self.cred, {
            'databaseURL': 'https://online-boogaloo.firebaseio.com/',
        })

        self.ref = db.reference()
        self.data = self.ref.get()

    #def get_latest(self):
        #self.data = self.ref.get()
        #at_stamp = 0
        #for point in self.data:
            #data_point = self.data[point]
            #if lat_stamp < data_point['timestamp']:
                #lat_stamp = data_point['timestamp']
                #latest = data_point

    #date = None
    #ruuvi_id = None
    def get_latest(self, latest):
        air_pressure = []
        humidity = []
        temperature = []
        times = []
        #Latest is what the user has selected in Telegram bot. We also need 2 times the datapoints because we have two ruuvitags. Data is delivered into database every 10 minutes
        if latest == "latest from fridge" or latest == "latest from inside":
            datapoints = 2 
        elif latest == "hour from fridge" or latest == "hour from inside":
            datapoints = 12
        self.data = self.ref.order_by_child('timestamp').limit_to_last(datapoints).get()
        for point in self.data:
            data_point = self.data[point]
            ruuvi_id = data_point["id"]
            #We only want the data what user wants
            con1 = "fridge" in latest and ruuvi_id == "ruuvi-1"
            con2 = "inside" in latest and ruuvi_id == "ruuvi-2"
            if con1 or con2:
                air_pressure.append(data_point["air-pressure"])
                humidity.append(data_point["humidity"])
                temperature.append(data_point["temperature"])
                stamp = data_point['timestamp']
                times.append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stamp)))
            
        #air_pressure = latest['air-pressure']
        #humidity = latest['humidity']
        #ruuvi_id = latest['id']
        #temperature = latest['temperature']
        #date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(latest['timestamp']))
        #return air_pressure, humidity, ruuvi_id, temperature, date
        return air_pressure, humidity, temperature, times
