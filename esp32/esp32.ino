#include <FirebaseESP32.h>
#include <FirebaseJson.h>

/*
 *  This sketch sends data via HTTP GET requests to data.sparkfun.com service.
 *
 *  You need to get streamId and privateKey at data.sparkfun.com and paste them
 *  below. Or just customize this script to talk to other HTTP servers.
 *
 */

#include <WiFi.h>

#define FIREBASE_HOST "online-boogaloo.firebaseio.com/" //Change to your Firebase RTDB project ID e.g. Your_Project_ID.firebaseio.com
#define FIREBASE_AUTH "f2tw35fx2P6v1vf3NkkyP0hamRoXv2cW1k4To4pn" //Change to your Firebase RTDB secret password

const char* ssid     = "your-ssid";
const char* password = "your-password";

const char* host = "data.sparkfun.com";
const char* streamId   = "....................";
const char* privateKey = "....................";

FirebaseData firebaseData1;
FirebaseData firebaseData2;


String path = "/ruuvidata";
String nodeID = "Node1"; 

void streamCallback(StreamData data)
{

  if (data.dataType() == "boolean") {
    if (data.boolData())
      Serial.println("Set to High");
    else
      Serial.println("Set to Low");
  }
}


void streamTimeoutCallback(bool timeout)
{
  if (timeout)
  {
    Serial.println();
    Serial.println("Stream timeout, resume streaming...");
    Serial.println();
  }
}


void setup()
{
    Serial.begin(115200);
    delay(10);
    randomSeed(analogRead(0)+analogRead(1));

    // We start by connecting to a WiFi network

    Serial.println();
    Serial.println();
    Serial.print("Connecting to ");
    Serial.println(ssid);

    WiFi.begin(ssid, password);

    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }

    Serial.println("");
    Serial.println("WiFi connected");
    Serial.println("IP address: ");
    Serial.println(WiFi.localIP());

    Serial.println("Connecting to firebase");
    Serial.println("host address: ");
    Serial.println(FIREBASE_HOST);
    
    Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);
    Firebase.reconnectWiFi(true);

    if (!Firebase.beginStream(firebaseData1, path + "/" + nodeID))
    {
      Serial.println("Could not begin stream");
      Serial.println("REASON: " + firebaseData1.errorReason());
      Serial.println();
    }
    Firebase.setStreamCallback(firebaseData1, streamCallback, streamTimeoutCallback);
}

int value = false;

void loop()
{
    FirebaseJson json1;
    delay(5000);
    value = !value;
    json1.add("air-pressure", 1040);
    json1.add("humidity", 23);
    json1.add("ruuviId", "ruuvis");
    json1.add("temperature", 15);
    String node = uudi4();

    if (Firebase.setBool(firebaseData2, path + "/" + nodeID, value)) {
      if (value)
        Serial.println("Set " + nodeID + " to High");
      else
        Serial.println("Set " + nodeID + " to Low");
    } else {
      Serial.println("Could not set ");
    }
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
