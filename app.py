from flask import Flask, render_template, request, redirect
from time import sleep
from thermostat import thermostat
from rfRemote import rfSend
import sys
from multiprocessing import Process
from flowTest2 import dispense_water

app = Flask(__name__)

def readConf():
	list = []
	try:
		with open('config.txt', 'r') as fileHandle:
			for line in fileHandle:
				currentPlace = line[:-1]
				list.append(currentPlace)
			return list
			fileHandle.close()
	except IOError:
		defaultList = [75, 50]
		writeConf(defaultList)
		file.close()

def writeConf(list):
	with open('config.txt', 'w') as fileHandle:
		for listitem in list:
			fileHandle.write('%s\n' % listitem)
		fileHandle.close()

@app.route("/", methods=["GET", "POST"])
def main_page():
	list = readConf()
	setTemperature = int(list[0])
	setHumidity = int(list[1])
	temperature, humidity, heaterStatus, humidifierStatus = thermostat(setTemperature, setHumidity)
	if request.method == 'POST':
		list = readConf()
		setTemperature = int(list[0])
		setHumidity = int(list[1])
		reqTemp = request.form['newTemperature']
		reqHumidity = request.form['newHumidity']
		if reqTemp == '':
			pass
		else:
			setTemperature = int(reqTemp)
		if reqHumidity == '':
			pass
		else:
			setHumidity = int(reqHumidity)
			print(reqHumidity)
		list = [setTemperature, setHumidity]
		writeConf(list)
		return redirect(request.url)
	elif request.method == 'GET': 
		return render_template("homeTemplate.html", temperature=temperature, humidity=humidity, heaterStatus=heaterStatus, humidifierStatus=humidifierStatus, setHumidity=setHumidity, setTemperature=setTemperature)

@app.route('/water', methods=['GET', 'POST'])
def watering_page():
	if request.method == 'POST':
		quantity = request.form['volume']
		#dispense_water(int(quantity))
		print(str(quantity) + ' Liters dispensed')
		return redirect(request.url)
	elif request.method == 'GET':
		return render_template('waterControl.html')

def startSite():
	app.run(host='0.0.0.0', port=2000, debug=True)
if __name__ == "__main__":
	webServer = Process(target=startSite)
	webServer.start()
	while True:
		try:
			list = readConf()
			setTemperature = int(list[0])
			setHumidity = int(list[1])
			temperature, humidity, heaterStatus, humidifierStatus = thermostat(setTemperature, setHumidity)
			print(str(temperature) + " F\n" + str(humidity) + " RH\n" + "Heater PWR: " + str(heaterStatus) + "\nHumidifier PWR: " + str(humidifierStatus))
			print(str(setTemperature) + " " + str(setHumidity))
			sleep(3)
		except KeyboardInterrupt:
			webServer.terminate()
			rfSend(1)
			rfSend(3)
			sys.exit()