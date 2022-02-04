from rpi_rf import RFDevice
#button1On = 5330227 #use button 1 for heater
#button1Off = 5330236
#button2On = 5330371 #use button 2 for humidifier
#button2Off = 5330380
#button3On = 5330691
#button3Off = 5330700
#button4On = 5332227
#button4Off = 5332236
#button5On = 5338371
#button5Off = 5338380
buttons = [5330227, 5330236, 5330371, 5330380, 5330691, 5330700, 5332227, 5332236, 5338371, 5338380]
def rfSend(code):
	#RF settings
	code = buttons[code]
	rfdevice = RFDevice(17)
	rfdevice.enable_tx()
	rfdevice.tx_repeat = 10
	pulseLength = 170
	protocol = 1
	#Send function
	rfdevice.tx_code(code, protocol, pulseLength, 24)