# Import SDK packages
from time import sleep

import datetime as datetime
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import aws_publish_raspberry_script as core
import RPi.GPIO as GPIO

import log_util

GPIO.setmode(GPIO.BOARD)

# Pin setting
moisture_pin = 0
ldr_pin = 7

# SPI configuration (moisture):
SPI_PORT = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))


# Read MCP3008 data
def moisture_reading(channel):
    i = 0
    data = []
    while i < 1000:
        value = mcp.read_adc_difference(channel)
        if value != 0:
            measure = (value/1023)*100
            data.append(measure)
            i += 1
    return round(100-(sum(data) / len(data)), 2)


# Read LDR data
def light_reading(channel):
    i = 0
    data = []
    while i < 100:
        measure = 0.0  # Output on the pin for
        GPIO.setup(channel, GPIO.OUT)
        GPIO.output(channel, GPIO.LOW)
        sleep(0.1)  # Change the pin back to input
        GPIO.setup(channel, GPIO.IN)  # Count until the pin goes high
        while GPIO.input(channel) == GPIO.LOW:
            measure += 1
        i += 1
        data.append(measure)
    return round((sum(data) / len(data)), 2)


# Keep reading the data from the Sensors
while True:
    try:
        moisture = moisture_reading(moisture_pin)
        light = light_reading(ldr_pin)
        log_util.log_debug(__name__, "Moisture reading: {}".format(moisture))
        log_util.log_debug(__name__, "Light reading: {}".format(light))
        message = {}
        message["id"] = 'id_smartgarden'
        now = datetime.datetime.now()
        message["datetimeid"] = now.isoformat()
        message['Items'] = {"moisture1": moisture,
                            "temperature": 0,
                            "humidity": 0,
                            "light": light}

        core.publish_readings(message)
        sleep(10)
    except KeyboardInterrupt as e:
        log_util.log_error(__name__, "Failed to read the data from the sensor due to {}".format(str(e)))
        break
    finally:
        GPIO.cleanup()
