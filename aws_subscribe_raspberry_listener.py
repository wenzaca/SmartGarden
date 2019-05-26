# Import SDK packages
import json
from time import sleep

import aws_publish_raspberry_core as core
import validate_sensors_values as sensors
import watering_relay_event as water
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import repository_dynamo
import validate_sensors_values

host = "arkau3u0cw2s4-ats.iot.eu-west-1.amazonaws.com"
rootCAPath = "certs/rootca.pem"
certificatePath = "certs/certificate.pem.crt"
privateKeyPath = "certs/private.pem.key"

automatic = False


def status_subscribe_action(client, userdata, message):
    global automatic
    print('Received a message: {}'.format(message.payload))
    byte_payload = message.payload.decode('utf8').replace("'", '"')
    data = json.loads(byte_payload)
    status = data['status']
    if status == 'A':
        automatic = True
    elif status == 'M':
        automatic = False
    elif status == 'F':
        watering = {
            "action": "OFF",
            "requester": "MANUAL"
        }
        core.publish_watering(watering)
    elif status == 'O':
        watering = {
            "action": "ON",
            "requester": "MANUAL"
        }
        core.publish_watering(watering)


def watering_subscribe_action(client, userdata, message):
    print('Received a message: {}'.format(message.payload))
    byte_payload = message.payload.decode('utf8').replace("'", '"')
    data = json.loads(byte_payload)
    water.watering_invocation(data)

def max_data_update_action(client, userdata, message):
    print('Received a message: {}'.format(message.payload))
    byte_payload = message.payload.decode('utf8').replace("'", '"')
    data = json.loads(byte_payload)
    validate_sensors_values.update_sensor_value(data)


def readings_subscribe_action(client, userdata, message):
    print('Received a message: {}'.format(message.payload))
    byte_payload = message.payload.decode('utf8').replace("'", '"')
    data = json.loads(byte_payload)
    if automatic:
        if sensors.moisture_level(data['Items']):
            data = {
                "action": "ON",
                "requester": "AUTOMATIC"
            }
            water.watering_invocation(data)
        else:
            print('The soil is too wet, the moisture level is {}'.format(data['Items']['moisture1']))


my_rpi = AWSIoTMQTTClient("Raspberry_Listener")
my_rpi.configureEndpoint(host, 8883)
my_rpi.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

my_rpi.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
my_rpi.configureDrainingFrequency(2)  # Draining: 2 Hz
my_rpi.configureConnectDisconnectTimeout(10)  # 10 sec
my_rpi.configureMQTTOperationTimeout(5)  # 5 sec

# Connect and subscribe to AWS IoT
my_rpi.connect()
my_rpi.subscribe('smartgarden/status', 1, status_subscribe_action)
my_rpi.subscribe('smartgarden/watering', 1, watering_subscribe_action)
my_rpi.subscribe('smartgarden/readings', 1, readings_subscribe_action)
my_rpi.subscribe('smartgarden/maxdata', 1, max_data_update_action)


if repository_dynamo.get_status()[0]['status'] == 'A':
    automatic = True


# Publish to the same topic in a loop forever
while True:
    pass





