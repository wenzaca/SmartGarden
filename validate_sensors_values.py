#!/usr/bin/env python3

temperature = 0
moisture = 0
humidity = 0


def moisture_level(data):
    global moisture
    return data['moisture1'] <= moisture


def temperature_too_high_level(data):
    global temperature
    return data['temperature'] > temperature


def update_sensor_value(data):
    global temperature
    global moisture
    global humidity
    temperature = data['temperature']
    humidity = data['humidity']
    moisture = data['moisture']
