# Smart Garden
Smart Garden - IoT Project

## About
The smart garden monitors the temperature, humidity, light levels and soil moisture of the plant. It has an automated system that waters the plant when the soil moisture is below an specific value and switches on the fan when the air temperature or humidity are below or above an specific value. This maintains an ideal and consistent soil condition for the plant, and makes it convenient for those who tend to forget to water their plants regularly.

We will be using a Raspberry Pi to receive data from the sensors and control the different actuators. The surrounding temperature, air humidity and brightness and soil moisture values will be recorded. These values will then be displayed on a web page, which allow users to know the environmental conditions of the plants when they check on them.

When the soil moisture level goes below the user input, and the automatic button is tuned on, the water pump will start to run and pump water into the soil automatically. This is very convenient for users as they do not need to water their plants every time but instead let the system water their plants automatically based on the moisture level of the soil.

As for the fans, when the temperature is above the specific or the air humidity is below the specified, the fans will turn on to allow the exchange of air with the outside environment. Mind that the system is inside of a Hydroponic tent.

The Light will be turned on constantly based on time (3, 6 or 9 hours) as manual input on the own light timer.

The temperature, humidity, light levels and soil moisture values will also be published to DynamoDB. Through a server (Raspberry Pi), the data will be displayed onto a flask web page where it shows real-time data coming from the sensors. This will allow users to view the real-time environmental conditions of the plants on the go (the latest 15 records through a graph).

The web page will also allow users to control the water pump and fans whenever the user decide, based on the automatically or manually input. The web page also counts with authorization based on username and password stored in a Cognito UserPool.

The user can also change the inputs values for turning on the fans and the water pump on the web page. By choosing Setting, the user can change the values of temperature, air humidity and moisture.

The user is also able to control the system using Alexa assistant. Check the SmartGarden CodeStar [project](https://github.com/wenzaca/SmartGardenAlexa) for more information.

The server that runs on the Raspberry PI is available on a third [project](https://github.com/wenzaca/SmartGardenRaspberry) that the user can download and run it on the Raspberry PI. For how to setup the hardware of this project, ensure to check the Raspberry project.

### Cloud
- AWS IoT:
    - Things:
        - Raspberry_Listener
        - Raspberry_Core
        - Raspberry_Readings
    - Topics:
        - smartgarden/status
        - smartgarden/maxdata
        - smartgarden/readings
        - smartgarden/watering
        - smartgarden/fans
    - Act (Rules):
        - smartgarden_status
        - smartgarden_fans
        - smartgarden_watering
        - smartgarden_readings
        - smartgarden_maxdata
    - Certificate
- DynamoDB:
    - smartgarden_maxdata (id)
    - smartgarden_readings (id, date)
    - smartgarden_status (id, date)
- Cognito UserPool
- EC2
- Route 53
- Alexa Custom Skill
- Lambda Function for the Custom Skills

## Schematic

![Cloud Schematic](src/flaskapp/static/img/aws.png)

## How to run
Ensure to have:
- Installed python3.
- Installed and configured your AWS CLI (with a role that has permission to access Dynamodb, AWS IoT and S3 Bucket).
- Have an S3 Bucket with the certificates in the following name pattern:
    - 'rootca.pem' the Root CA certificate;
    - 'certificate.pem.crt' for the IoT Certificate attached to the things;
    - 'private.pem.key' for the private key attached to the things.
- Virtual Environment
     - ```python3 -m venv .venv```
     - ```source .venv/bin/activate```
     - ```pip3 install SmartGarden```

To run:
- Server:
    - ```pip3 setup.py install```
    - Locally:```sudo nohup smart_garden [-h] [--profile_name PROFILE_NAME] --s3-bucket S3_BUCKET [--aws_region AWS_REGION] --port 5000```
    - Not Locally: ```sudo nohup smart_garden [-h] [--profile_name PROFILE_NAME] --s3-bucket S3_BUCKET [--aws_region AWS_REGION] --port 80```
    
Useful commands:
- Get IP: ```ping raspberrypi.local```
- Connect: ```ssh pi@IP```
- Transfer File: ```scp filename pi@IP:/home/pi```
- Find server process (MAC): ```netstat -vanp tcp | grep 5000```
- Kill process: ```kill [port number]```

## How to Deploy
- Generete the Distribution file: ```python3 setup.py install bdist_wheel --universal sdist```
- Upload to Pypi: ```twine upload dist/*```
- Upload to Pypi Test: ```twine upload --repository-url https://test.pypi.org/legacy/ dist/*```


## References
- [Project Reference](https://www.hackster.io/mokxf16/smart-garden-raspberry-pi-arduino-65c7b7)
- [Raspberry Server](https://github.com/wenzaca/SmartGardenRaspberry)
- [Alexa Custom Skill](https://github.com/wenzaca/SmartGardenAlexa)