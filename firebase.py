import firebase_admin
import time
from firebase_admin import credentials
from firebase_admin import db


class DataBase:

    def __init__(self):
        # Use the application default credentials
        self.cred = credentials.Certificate('online-boogaloo-firebase-adminsdk-7qkz5-1d8b512e88.json')
        firebase_admin.initialize_app(self.cred, {
            'databaseURL': 'https://online-boogaloo.firebaseio.com/',
        })

        self.ref = db.reference()
        self.data = self.ref.get()

    def get_latest(self):
        lat_stamp = 0
        for point in self.data:
            data_point = self.data[point]
            if lat_stamp < data_point['timestamp']:
                lat_stamp = data_point['timestamp']
                latest = data_point

        air_pressure = latest['air-pressure']
        humidity = latest['humidity']
        ruuvi_id = latest['id']
        temperature = latest['temperature']
        date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(latest['timestamp']))
        return air_pressure, humidity, ruuvi_id, temperature, date
