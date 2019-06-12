# Import SDK packages
from time import sleep

import datetime as datetime
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import aws_publish_raspberry_script as core

import log_util

# Start SPI connection


# SPI configuration:
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
            measure = (measure/1023)*100
            data[i] = measure
            i += 1
    return sum(data) / len(data)


# Publish to the same topic in a loop forever
while True:
    try:
        moisture = moisture_reading(0)
        log_util.log_info(__name__, "Moisture reading: {}".format(moisture))
        message = {}
        now = datetime.datetime.now()
        message["datetimeid"] = now.isoformat()
        message['Items'] = {"moisture1": moisture,
                            "temperature": 0,
                            "humidity": 0,
                            "light": 0}

        core.publish_readings(message)
        sleep(10)
    except KeyboardInterrupt as e:
        log_util.log_error(__name__, "Failed to read the data from the sensor due to {}".format(str(e)))
