# Import SDK packages
import datetime as datetime
import json
import sys

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

host = "arkau3u0cw2s4-ats.iot.eu-west-1.amazonaws.com"
rootCAPath = "certs/rootca.pem"
certificatePath = "certs/certificate.pem.crt"
privateKeyPath = "certs/private.pem.key"

# Stablishing MQTT Connection
my_rpi = AWSIoTMQTTClient("Fake_Publish")
my_rpi.configureEndpoint(host, 8883)
my_rpi.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# mosquitto_sub -h arkau3u0cw2s4-ats.iot.eu-west-1.amazonaws.com -p 8883 -k 60 -i Raspberry_Core --cafile rootca.pem --cert certificate.pem.crt  --key private.pem.key -t 'smartgarden/readings' -d

my_rpi.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
my_rpi.configureDrainingFrequency(2)  # Draining: 2 Hz
my_rpi.configureConnectDisconnectTimeout(10)  # 10 sec
my_rpi.configureMQTTOperationTimeout(5)  # 5 sec

# Connect and subscribe to AWS IoT
my_rpi.connect()

# Publish to the same topic in a loop forever

message = {}
message["id"] = 'id_smartgarden'

now = datetime.datetime.now()
message["datetimeid"] = now.isoformat()
message['Items'] = {"moisture1": int(sys.argv[1]),
                    "temperature": 30,
                    "humidity": 80,
                    "light": 50}

print(json.dumps(message))

my_rpi.publish("smartgarden/readings", json.dumps(message), 1)
