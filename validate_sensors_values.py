#!/usr/bin/env python3

import repository_dynamo

temperature = 0
moisture = 0
humidity = 0


def moisture_level(data):
    global moisture
    return data['moisture1'] <= int(moisture)


def temperature_too_high_level(data):
    global temperature
    return data['temperature'] > temperature


def update_sensor_value(data):
    global temperature
    global moisture
    global humidity
    temperature = data['Items'][0]['temperature']
    humidity = data['Items'][0]['humidity']
    moisture = data['Items'][0]['moisture']


update_sensor_value(repository_dynamo.get_max_data())
