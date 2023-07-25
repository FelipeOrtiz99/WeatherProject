// #include <Time.h>
// #include <TimeLib.h>

#include <Ticker.h>
#include "DHT.h"
#include <Wire.h>
#include <RTClib.h>
#include <String.h>

#define DHTPIN 2
#define DHTTYPE DHT11
#define ANMMTRO A2
#define HLGF A1


int insolacion = 0;
int insolacionTotal = 0;
String arrayTemperatura = "";
String arrayHumedad = "";
String arrayVelViento = "";
DateTime fechaInicial;

void fnVaribles(){
  float temperatura = getTemperatura();
  arrayTemperatura.concat(String(temperatura)+",");
  float humedad = getHumedad();
  arrayHumedad.concat(String(humedad)+",");
  float velViento =  getVelocidadViento();
  arrayVelViento.concat(String(velViento)+",");
  Serial.println("temperature:" + String(temperatura) + " " + "humidity:" + String(humedad) + " " + "vel:" + String(velViento) + " " + "rad:" + String(insolacion));
  insolacionTotal += insolacion;
  insolacion = 0;
  }

void fnInsolacion(){
  float lectura = analogRead(A1);
  float volt = lectura / 1023 * 5000.0;
  if (volt >= 3000.0) {
    insolacion++;
  }
}

Ticker tickVariables(fnVaribles,5000);
Ticker tickInsolacion(fnInsolacion,1000);
DHT dht(DHTPIN, DHTTYPE);
RTC_DS3231 rtc;

float getTemperatura(){
  float temperatura = dht.readTemperature();
  if (isnan(temperatura)) {
    Serial.println("Error obteniendo los datos del sensor DHT11");
    return;
  }
  return temperatura;
}

float getHumedad(){
  float humedad = dht.readHumidity();
  if (isnan(humedad)) {
    Serial.println("Error obteniendo los datos del sensor DHT11");
    return;
  }
  return humedad;
}

float getVelocidadViento(){
  float lectura = analogRead(ANMMTRO);
  float velocidad = (lectura * 0.63);
  return velocidad;
}


void setup() {  
  // put your setup code here, to run once:
  Serial.begin(9600);
  // pinMode(ANMMTRO,INPUT);   
  // pinMode(HLGF,INPUT);
  dht.begin();
  tickVariables.start();
  tickInsolacion.start();

  Wire.begin();
  if (!rtc.begin()) {
  Serial.println("Modulo RTC no encontrado");
  while(1);
  }
  
  rtc.adjust(DateTime(__DATE__, __TIME__));
  fechaInicial = rtc.now();
}

void loop() {
  // put your main code here, to run repeatedly:
  tickVariables.update();
  tickInsolacion.update();
  DateTime fechaHora = rtc.now();
  
  if (fechaInicial.hour() != fechaHora.hour()) {
    tickVariables.stop();
    tickVariables.start();
    fechaInicial = rtc.now();
    arrayTemperatura.remove(arrayTemperatura.length() - 1);
    arrayHumedad.remove(arrayHumedad.length() - 1);
    arrayVelViento.remove(arrayVelViento.length() - 1);
    Serial.println("temperature:" + arrayTemperatura + " " + "humidity:" + arrayHumedad + " " + "vel:" + arrayVelViento + " " + "rad:" + String(insolacionTotal) + "eto:");
    insolacionTotal = 0;
  }
}
