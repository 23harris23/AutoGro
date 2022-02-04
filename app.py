from flask import Flask
from time import sleep
from thermostat import thermostat
from rfRemote import rfSend
import sys
from multiprocessing import Process
setTempertaure = 67
setHumidity = 50
app = Flask(__name__)
@app.route("/")
def main_page():
	temperature, humidity, heaterStatus, humidifierStatus = thermostat(setTempertaure, setHumidity)
	return("</p>" + str(temperature) + " F\n" + str(humidity) + " RH\n" + "Heater PWR: " + str(heaterStatus) + "\nHumidifier PWR: " + str(humidifierStatus) + "</p>")
def startSite():
	app.run(host='0.0.0.0' port=2000)
if __name__ == "__main__":
	webServer = Process(target=startSite)
	webServer.start()
	while True:
		try:
			temperature, humidity, heaterStatus, humidifierStatus = thermostat(setTempertaure, setHumidity)
			print(str(temperature) + " F\n" + str(humidity) + " RH\n" + "Heater PWR: " + str(heaterStatus) + "\nHumidifier PWR: " + str(humidifierStatus))
			sleep(3)
		except KeyboardInterrupt:
			webServer.terminate()
			rfSend(1)
			rfSend(3)
			sys.exit()