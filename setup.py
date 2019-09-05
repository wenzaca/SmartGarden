# -*- coding: utf-8 -*-

import os

from setuptools import setup

long_description="Smart Garden - IoT Project" \
                 "" \
                 "" \
                 "The smart garden monitors the temperature, humidity, light levels and soil moisture of the plant. It has an automated system that waters the plant when the soil moisture is below an specific value and switches on the fan when the air temperature or humidity are below or above an specific value. This maintains an ideal and consistent soil condition for the plant, and makes it convenient for those who tend to forget to water their plants regularly." \
                 "" \
                 "We will be using a Raspberry Pi to receive data from the sensors and control the different actuators. The surrounding temperature, air humidity and brightness and soil moisture values will be recorded. These values will then be displayed on a web page, which allow users to know the environmental conditions of the plants when they check on them." \
                 "" \
                 "When the soil moisture level goes below the user input, and the automatic button is tuned on, the water pump will start to run and pump water into the soil automatically. This is very convenient for users as they do not need to water their plants every time but instead let the system water their plants automatically based on the moisture level of the soil." \
                 "" \
                 "As for the fans, when the temperature is above the specific or the air humidity is below the specified, the fans will turn on to allow the exchange of air with the outside environment. Mind that the system is inside of a Hydroponic tent." \
                 "" \
                 "The Light will be turned on constantly based on time (3, 6 or 9 hours) as manual input on the own light timer." \
                 "" \
                 "The temperature, humidity, light levels and soil moisture values will also be published to DynamoDB. Through a server (Raspberry Pi), the data will be displayed onto a flask web page where it shows real-time data coming from the sensors. This will allow users to view the real-time environmental conditions of the plants on the go (the latest 15 records through a graph)." \
                 "" \
                 "The web page will also allow users to control the water pump and fans whenever the user decide, based on the automatically or manually input. The web page also counts with authorization based on username and password stored in a Cognito UserPool." \
                 "" \
                 "The user can also change the inputs values for turning on the fans and the water pump on the web page. By choosing Setting, the user can change the values of temperature, air humidity and moisture." \
                 "" \
                 "The user is also able to control the system using Alexa assistant. Check the SmartGarden CodeStar [project](https://github.com/wenzaca/SmartGardenAlexa) for more information." \
                 "" \
                 "The server that runs on the Raspberry PI is available on a third [project](https://github.com/wenzaca/SmartGardenRaspberry) that the user can download and run it on the Raspberry PI. For how to setup the hardware of this project, ensure to check the Raspberry project."


with open('LICENSE') as f:
    license = f.read()

setup(
    name="SmartGarden",
    version="1.0.1",
    description="Smart Garden Webserver used to control an Raspberry PI, developed in Python with JS, Jquery and Ajax.",
    author='Wendler Zacariotto',
    author_email='wenzaca@gmail.com',
    url='https://github.com/wenzaca/SmartGarden',
    long_description=long_description,
    license=license,
    keywords=['SmartGarden', 'aws', 'Raspberry'],

    # declare your packages
    packages=["src", "src.flaskapp", "src.flaskapp.static.css", "src.flaskapp.templates", "src.flaskapp.static.js",
              "src.flaskapp.static.img", "src.flaskapp.static.fonts", "conf"],

    # include data files
    include_package_data=True,
    exclude_package_data={'': ['.DS_Store']},

    # requirements
    install_requires=['Flask>1.0', 'boto3>1.9.100', 'AWSIoTPythonSDK>1.4.0', 'numpy>1.17.0', 'flask_wtf>0.14.0'],
    python_requires='>=3.6.0',

    # run
    test_suite="test",
    entry_points={'console_scripts': [
                       'smart_garden = src.command_line:main'
                   ]
               }


)
