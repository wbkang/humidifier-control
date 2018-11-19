#!/usr/bin/env python3

from RPi import GPIO
import time
from dht11.dht11 import DHT11
import requests


DHT11_PIN = 4
HUMIDITY_OFFSET = 10 # add this much to the REAL humidity
HUMIDITY_THRESHOLD = 50

GPIO.setmode(GPIO.BCM)

sensor = DHT11(DHT11_PIN)

humidifier_status = None

def control_humidifier(onoff):
    global humidifier_status
    if onoff != humidifier_status:
        print("Controlling humidifier %s" % onoff)
        requests.post("http://localhost:6001/lights/humidifier/%s" % ("on" if onoff else "off"))
        humidifier_status = onoff
        return True
    return False

while True:
    max_humidity = 0
    for _ in range(10):
        record = sensor.read()
        if record.is_valid():
            max_humidity = max(record.humidity, max_humidity)
        time.sleep(1)
    
    max_humidity += HUMIDITY_OFFSET
    print("Current humidity is %f" % max_humidity)
    onoff = max_humidity <= HUMIDITY_THRESHOLD
    changed = control_humidifier(onoff)
    if changed and not onoff:
        # just changed to OFF
        print("Just turned off, waiting for 30 minutes before next check")
        time.sleep(60 * 30)
    else:
        print ("next check in 5 min")
        time.sleep(300)
