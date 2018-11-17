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

while True:
    max_humidity = 0
    for _ in range(10):
        record = sensor.read()
        if record.is_valid():
            max_humidity = max(record.humidity, max_humidity)
        time.sleep(1)
    
    max_humidity += HUMIDITY_OFFSET
    print("Current humidity is %f" % max_humidity)
    control_humidifier(max_humidity <= HUMIDITY_THRESHOLD)
    
