import datetime as datetime
from datetime import date

import log_util

import aws_publish_raspberry_server as core
import boto3


def login():
    try:
        dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')
        table = dynamodb.Table('smartgarden_login')
        response = table.scan()

        items = response['Items']

        return items
    except:
        import sys
        log_util.log_error(__name__, sys.exc_info()[0])
        log_util.log_error(__name__, sys.exc_info()[1])


def post_max_data(data):
    try:
        new_data = {
            "id": "id_smartgarden",
            "Items": [data]
        }
        core.publish_max_data(new_data)
    except:
        import sys
        log_util.log_error(__name__, sys.exc_info()[0])
        log_util.log_error(__name__, sys.exc_info()[1])


def get_max_data():
    try:
        dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')
        table = dynamodb.Table('smartgarden_maxdata')

        response = table.query(KeyConditionExpression='id = :id_smartgarden',
                               ExpressionAttributeValues={
                                   ':id_smartgarden': 'id_smartgarden'},
                               ScanIndexForward=False
                               )

        items = response['Items']

        n = 1  # get latest data
        data = items[:n]
        return data[0]
    except:
        import sys
        log_util.log_error(__name__, sys.exc_info()[0])
        log_util.log_error(__name__, sys.exc_info()[1])


def get_data():
    try:
        dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')
        table = dynamodb.Table('smartgarden_readings')

        startdate = date.today().isoformat()
        response = table.query(KeyConditionExpression='id = :id_smartgarden AND datetimeid >= :begindate',
                               ExpressionAttributeValues={
                                   ':id_smartgarden': 'id_smartgarden',
                                   ':begindate': startdate},
                               ScanIndexForward=False
                               )

        items = response['Items']

        n = 1  # get latest data
        data = items[:n]
        return data
    except:
        import sys
        log_util.log_error(__name__, sys.exc_info()[0])
        log_util.log_error(__name__, sys.exc_info()[1])


def get_chart_data():
    try:

        dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')
        table = dynamodb.Table('smartgarden_readings')

        startdate = date.today().isoformat()
        response = table.query(KeyConditionExpression='id = :id_smartgarden AND datetimeid >= :begindate',
                               ExpressionAttributeValues={
                                   ':id_smartgarden': 'id_smartgarden',
                                   ':begindate': startdate},
                               ScanIndexForward=False
                               )

        items = response['Items']

        n = 15  # limit to last 15 items
        data = items[:n]
        data_reversed = data[::-1]
        return data_reversed
    except:
        import sys
        log_util.log_error(__name__, sys.exc_info()[0])
        log_util.log_error(__name__, sys.exc_info()[1])


def get_status():
    try:
        dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')
        table = dynamodb.Table('smartgarden_status')

        startdate = date.today().isoformat()
        response = table.query(KeyConditionExpression='id = :id_smartgarden AND datetimeid >= :begindate',
                               ExpressionAttributeValues={
                                   ':id_smartgarden': 'id_status',
                                   ':begindate': startdate},
                               ScanIndexForward=False
                               )

        items = response['Items']

        n = 1
        data = items[:n]
        return data
    except:
        import sys
        log_util.log_error(__name__, sys.exc_info()[0])
        log_util.log_error(__name__, sys.exc_info()[1])


def post_status(status):
    try:
        now = datetime.datetime.now()
        new_item = {
            "id": "id_status",
            'datetimeid': now.isoformat(),
            'status': str(status)
        }
        core.publish_status(new_item)
    except:
        import sys
        log_util.log_error(__name__, sys.exc_info()[0])
        log_util.log_error(__name__, sys.exc_info()[1])
