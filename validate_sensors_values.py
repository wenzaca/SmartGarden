#!/usr/bin/env python3

import repository_dynamo
import log_util

temperature = 0
moisture = 0
humidity = 0


def moisture_level(data):
    global moisture
    log_util.log_debug(__name__, "Checking moisture level, received {}, checking if it is above {}".format(
        data['moisture1'], moisture))
    return data['moisture1'] <= int(moisture)


def temperature_too_high_level(data):
    global temperature
    log_util.log_debug(__name__, "Checking temperature level, received {}, checking if it is above {}".format(
        data['temperature'], moisture))
    return data['temperature'] > temperature


def update_sensor_value(data):
    global temperature
    global moisture
    global humidity
    log_util.log_debug(__name__, "Updating sensor value, previous values were T:{}, H:{}, M:{}. New values are T:{}, "
                             "H:{}, M:{}".format(temperature,humidity,moisture, data['Items'][0]['temperature'],
                                                 data['Items'][0]['humidity'], data['Items'][0]['moisture']))
    temperature = data['Items'][0]['temperature']
    humidity = data['Items'][0]['humidity']
    moisture = data['Items'][0]['moisture']


update_sensor_value(repository_dynamo.get_max_data())
