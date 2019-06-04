# Import SDK packages
from time import sleep

import datetime as datetime
import spidev  # To communicate with SPI devices
import aws_publish_raspberry_core as core

import log_util

# Start SPI connection
spi = spidev.SpiDev()  # Created an object
spi.open(0, 0)


# Read MCP3008 data
def moisture_reading(channel):
    i = 0;
    data = []
    while i < 1000:
        val = spi.xfer2([1, (8 + channel) << 4, 0])
        measure = ((val[1] & 3) << 8) + val[2]
        if measure != 0:
            data[i] = measure
            i += 1
    return sum(data) / len(data)


# Publish to the same topic in a loop forever
while True:
    try:
        moisture = moisture_reading
        log_util.log_info(__name__, "Moisture reading: {}".format(moisture))
        message = {}
        now = datetime.datetime.now()
        message["datetimeid"] = now.isoformat()
        message['Items'] = {"moisture1": moisture,
                            "temperature": 0,
                            "humidity": 0,
                            "light": 0}

        core.publish_readings(message)
        sleep(3000)
    except KeyboardInterrupt as e:
        log_util.log_error(__name__, "Failed to read the data from the sensor due to {}".format(str(e)))
