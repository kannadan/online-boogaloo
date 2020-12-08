#include <FirebaseESP32.h>
#include <FirebaseJson.h>

#include <WiFi.h>
#include "time.h"
#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEScan.h>
#include <BLEAdvertisedDevice.h>
#include <BLEAddress.h>

#define FIREBASE_HOST "online-boogaloo.firebaseio.com/" //Change to your Firebase RTDB project ID e.g. Your_Project_ID.firebaseio.com
#define FIREBASE_AUTH "f2tw35fx2P6v1vf3NkkyP0hamRoXv2cW1k4To4pn" //Change to your Firebase RTDB secret password


int scanTime = 5; //In seconds
BLEScan* pBLEScan;
int temp, hum, pressure, ax, ay, az, voltage_power, voltage, power, rssi_ruuvi, movement, measurement;

const char* ssid     = "OTiT";
const char* password = "oh8taoh8ta";

const char* ntpServer = "pool.ntp.org";

FirebaseData firebaseData2;


String path = "/ruuvidata";
String nodeID = "Node1";
 
String ruuvimac = "EB:3F:74:AB:F0:D7";


const long  gmtOffset_sec = 7200;
const int   daylightOffset_sec = 3600;


//Converts hexadecimal values to decimal values
int hexadecimalToDecimal(String hexVal)
{
    int len = hexVal.length();
    int base = 1;

    int dec_val = 0;

    for (int i = len - 1; i >= 0; i--)
    {
        if (hexVal[i] >= '0' && hexVal[i] <= '9')
        {
            dec_val += (hexVal[i] - 48) * base;

            base = base * 16;
        }
        else if (hexVal[i] >= 'A' && hexVal[i] <= 'F')
        {
            dec_val += (hexVal[i] - 55) * base;

            base = base * 16;
        }
    }
    return dec_val;
}

//Decodes RUUVI raw data and arranges it in an array
void decodeRuuvi(String hex_data, int rssi){
    if(hex_data.substring(4, 6) == "05"){
        temp = hexadecimalToDecimal(hex_data.substring(6, 10))*0.005;
        hum = hexadecimalToDecimal(hex_data.substring(10, 14))*0.0025;
        pressure = hexadecimalToDecimal(hex_data.substring(14, 18))*1+50000;
       
        ax = hexadecimalToDecimal(hex_data.substring(18, 22));
        ay = hexadecimalToDecimal(hex_data.substring(22, 26));
        az = hexadecimalToDecimal(hex_data.substring(26, 30));     

        if(ax > 0xF000){
          ax = ax - (1 << 16);
        }
        if(ay > 0xF000){
          ay = ay - (1 << 16);
        }
        if (az > 0xF000){
          az = az - (1 << 16);
        }

        voltage_power = hexadecimalToDecimal(hex_data.substring(30, 34));
        voltage = (int)((voltage_power & 0x0b1111111111100000) >> 5) + 1600;
        power = (int)(voltage_power & 0x0b0000000000011111) - 40;

        rssi_ruuvi = rssi;

        movement = hexadecimalToDecimal(hex_data.substring(34, 36));
        measurement = hexadecimalToDecimal(hex_data.substring(36, 40));
    }
}

void sendData(){
  Serial.print("Temperature: ");
  Serial.println(temp);
  Serial.print("Pressure: ");
  Serial.println(pressure);
  FirebaseJson json1;
  json1.add("air-pressure", pressure);
  json1.add("humidity", hum);
  json1.add("id", "ruuvi-1");
  json1.add("temperature", temp);
  json1.set("timestamp", (double) getTimeStamp());
  String node = uuid4();
  if (Firebase.setJSON(firebaseData2, "/" + node, json1)) {
    Serial.println(firebaseData2.dataType());
  } else {
    Serial.println("error sending");
    Serial.println(firebaseData2.errorReason());
  }
}

class MyAdvertisedDeviceCallbacks: public BLEAdvertisedDeviceCallbacks {
    void onResult(BLEAdvertisedDevice advertisedDevice) {
      //Scans for specific BLE MAC addresses 
      if(ruuvimac.indexOf(advertisedDevice.getAddress().toString().c_str()) >= 0){ //If the scanned MAC address is in the identified MAC address String
        String raw_data = String(BLEUtils::buildHexData(nullptr, (uint8_t*)advertisedDevice.getManufacturerData().data(), advertisedDevice.getManufacturerData().length()));
        raw_data.toUpperCase();
        decodeRuuvi(raw_data, advertisedDevice.getRSSI());     
        //sendData();  
      }  
    }
};

long getTimeStamp(){
  struct tm timeinfo;
  if(!getLocalTime(&timeinfo)){
    Serial.println("Failed to obtain time");
    return 0;
  }
  //Serial.println(&timeinfo, "%A, %B %d %Y %H:%M:%S");
  time_t now;
  time(&now);
  Serial.println(now);
  return now;
}


void setup()
{
    Serial.begin(115200);
    delay(10);
    randomSeed(analogRead(0)+analogRead(1));


    WiFi.begin(ssid, password);

    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    configTime(gmtOffset_sec, daylightOffset_sec, ntpServer);
    getTimeStamp();

    Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);
    Firebase.reconnectWiFi(true);
    
    ruuvimac.toLowerCase();
    BLEDevice::init("");
    pBLEScan = BLEDevice::getScan(); //create new scan
    pBLEScan->setAdvertisedDeviceCallbacks(new MyAdvertisedDeviceCallbacks());
    pBLEScan->setActiveScan(true); //active scan uses more power, but get results faster
    pBLEScan->setInterval(100);
    pBLEScan->setWindow(99);  // less or equal setInterval value
   
}

int value = false;
char incoming;
void loop()
{

    BLEScanResults foundDevices = pBLEScan->start(scanTime, false);
    pBLEScan->clearResults();   // delete results fromBLEScan buffer to release memory
    sendData();
    delay(600000);
}

String uuid4(){
  String res = "";
  res = res + hex_print(8,0,15);
  res = res + "-";
  Serial.print("-");
  res = res + hex_print(4,0,15);
  res = res + "-4";
  Serial.print("-");
  Serial.print("4");
  res = res + hex_print(3,0,15);
  res = res + "-";
  Serial.print("-");
  res = res + hex_print(1,8,11);
  res = res + hex_print(3,0,15);
  res = res + "-";
  Serial.print("-");
  res = res + hex_print(12,0,15);
  Serial.println("");
  return res;
}

String hex_print(int n,int mn ,int mx ){
  String res = "";
  for(;n>0;n--){
    int X = random(mn,mx);
    res = res + String(X, HEX);
    Serial.print ( X ,HEX );
  }
  return res;
}
