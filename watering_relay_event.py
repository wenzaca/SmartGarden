#!/usr/bin/env python3

# Import SDK packages
import RPi.GPIO as GPIO
import threading
# Import SDK packages
from time import sleep
import log_util

relay_pin = 20


GPIO.setmode(GPIO.BCM)
GPIO.setup(relay_pin, GPIO.OUT)
GPIO.output(relay_pin, 1)

def job(str):
    log_util.log_info(__name__, str)
    GPIO.output(relay_pin, 0)
    sleep(3.2)
    GPIO.output(relay_pin, 1)
    #sleep(58)
    return


def stopWatering(str):
    log_util.log_info(__name__, str)
    # GPIO.output(relay_pin, 1)


def watering_invocation(data):
    requester = "Turn {} requested by {}".format(data['action'], data['requester'])
    if 'ON' in data['action']:
        t = threading.Thread(target=job, args=(requester,))
        t.start()
    else:
        stopWatering(requester)


# schedule.every().day.at("06:00").do(job,'"Turn on requested by Scheduler')

'''
"{'action':'ON','requester':'alexa'}"
'''
