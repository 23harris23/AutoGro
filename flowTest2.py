#!/usr/bin/python
import RPi.GPIO as GPIO
import time, sys
from rfRemote import rfSend
#import paho.mqtt.publish as publish
FLOW_SENSOR_GPIO = 27

global count
count = 0
global start_counter
start_counter = 0 
def countPulse(channel):
   global count
   if start_counter == 1:
      count = count+1

def dispense_water(totalVolume):
    global count
    global start_counter
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(FLOW_SENSOR_GPIO, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.add_event_detect(FLOW_SENSOR_GPIO, GPIO.FALLING, callback=countPulse)
    while totalVolume >= 0:
        try:
            rfSend(4)
            start_counter = 1
            time.sleep(1)
            start_counter = 0
            flow = (count / 68.75) # Pulse frequency (Hz) = 7.5Q, Q is flow rate in L/min.
            print("The flow is: %.3f Liter/min" % (flow))
            #publish.single("/Garden.Pi/WaterFlow", flow, hostname=MQTT_SERVER)
            count = 0
            time.sleep(2)
            totalVolume = totalVolume - (flow * 0.05)
            #print(str(totalVolume) + " L left"
        except KeyboardInterrupt:
            print('\nkeyboard interrupt!')
            rfSend(5)
            GPIO.cleanup()
            sys.exit()
    rfSend(5)
    rfSend(5)
    rfSend(5)

if __name__ == "__main__":
    dispense_water(1)