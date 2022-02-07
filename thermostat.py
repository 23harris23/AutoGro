from rfRemote import rfSend
from time import sleep
import Adafruit_DHT
import sys

DHTpin = 22
heaterStatus = False
humidifierStatus = False

def getData():
	humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, DHTpin)

def thermostat(setTemperature, setHumidity):
	humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, DHTpin)
	while temperature is None and humidity is None:
		humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, DHTpin)

	temperature = (temperature * 1.8) + 32
	if temperature >= setTemperature:
		rfSend(1)
		heaterStatus = False
	else:
		rfSend(0)
		heaterStatus = True
	if humidity >= setHumidity:
		rfSend(2)
		humidifierStatus = False
	else:
		rfSend(3)
		humidifierStatus = True
	return temperature, humidity, heaterStatus, humidifierStatus

if __name__ == "__main__":
	while True:
		try:
			temperature, humidity, heaterStatus, humidifierStatus = thermostat(65, 50)
			print(str(temperature) + " F\n" + str(humidity) + " RH\n" + "Heat PWR" + str(heaterStatus) + "\nHumidifier PWR:" + str(humidifierStatus))
			sleep(5)
		except KeyboardInterrupt:
			rfSend(1)
			rfSend(3)
			print("Shutting down")
			sys.exit()