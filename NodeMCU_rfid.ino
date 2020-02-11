/* RC522 Interfacing with NodeMCU
 * 
 * Typical pin layout used:
 * ----------------------------------
 *             MFRC522      Node     
 *             Reader/PCD   MCU      
 * Signal      Pin          Pin      
 * ----------------------------------
 * RST/Reset   RST          D1 (GPIO5)        
 * SPI SS      SDA(SS)      D2 (GPIO4)       
 * SPI MOSI    MOSI         D7 (GPIO13)
 * SPI MISO    MISO         D6 (GPIO12)
 * SPI SCK     SCK          D5 (GPIO14)
 * 3.3V        3.3V         3.3V
 * GND         GND          GND
 */

#include <ESP8266WiFi.h>
#include <WiFiClient.h> 
#include <ESP8266WebServer.h>
#include <ESP8266HTTPClient.h>
#include "SPI.h" // SPI library
#include "MFRC522.h"


const char* ssid = "anuja";// Your wifi Name       
const char* password = "ar3k57u4";// Your wifi Password

const char *host = "192.168.43.212";
const int pinRST = 5;
const int pinSDA = 4;
int Led_OnBoard = 2;

MFRC522 mfrc522(pinSDA, pinRST); // Set up mfrc522 on the Arduino

void setup() {
  WiFi.mode(WIFI_OFF); //Prevents reconnection issue (taking too long to connect)
  delay(1000);
  WiFi.mode(WIFI_STA); //This line hides the viewing of ESP as wifi hotspot
  SPI.begin(); // open SPI connection
  mfrc522.PCD_Init(); // Initialize Proximity Coupling Device (PCD)
  Serial.begin(115200); // open serial connection
  WiFi.begin(ssid, password);     //Connect to your WiFi router
  Serial.print("Connecting");
  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    digitalWrite(Led_OnBoard, LOW);
    delay(250);
    Serial.print(".");
    digitalWrite(Led_OnBoard, HIGH);
    delay(250);
  }
  Serial.println(WiFi.localIP());
}

void loop() {
  HTTPClient http;    //Declare object of class HTTPClient
  String rfidNo, postData="";
  
  if (mfrc522.PICC_IsNewCardPresent()) { // (true, if RFID tag/card is present ) PICC = Proximity Integrated Circuit Card
    if(mfrc522.PICC_ReadCardSerial()) { // true, if RFID tag/card was read
      for (byte i = 0; i < mfrc522.uid.size; ++i) { // read id (in parts)
        Serial.print(mfrc522.uid.uidByte[i], HEX); // print id as hex values
        postData = postData + String(mfrc522.uid.uidByte[i],HEX);
        
      }
      Serial.print("postData: ");
      Serial.println(postData);
      Serial.println(); // Print out of id is complete.
      delay(1500);
        }
  //Post Data
  postData = "rfidNo=" + rfidNo;
  
  http.begin("http://192.168.43.212:8084/REST_Test/webresources/generic/50");              //Specify request destination
  http.addHeader("Content-Type", "application/x-www-form-urlencoded");    //Specify content-type header
 
  int httpCode = http.POST(postData);   //Send the request
  String payload = http.getString();    //Get the response payload
  Serial.println(httpCode);   //Print HTTP return code
  Serial.println(payload);    //Print request response payload
  Serial.print("RFID No= ");
  Serial.print(rfidNo);
  delay(2000);
  http.end();  //Close connection
}
 }
