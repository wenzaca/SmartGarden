# Import SDK packages
from time import sleep

# import spidev # To communicate with SPI devices
from numpy import interp  # To scale values


# Start SPI connection
# spi = spidev.SpiDev() # Created an object
# spi.open(0,0)

# Read MCP3008 data
def analogInput(channel):
    spi.max_speed_hz = 1350000
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    interp(data, [0, 1023], [100, 0])
    return int(data)


# Publish to the same topic in a loop forever
while True:
    sleep(0.001)
    # Read data from soil moisture sensor 1
    '''soilMoisture1 = 100 # Reading from CH0
    print("Moisture: {}%".format(soilMoisture1))


    loopCount = loopCount+1
    message = {}
    message["id"] = 'id_smartgarden'

    now = datetime.datetime.now()
    message["datetimeid"] = now.isoformat()
    message['Items'] = {"moisture1": soilMoisture1}

    core.publish_readings(message)
    '''
