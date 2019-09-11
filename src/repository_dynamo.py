import datetime as datetime

import boto3

from src import aws_publish_raspberry_server as core, log_util


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

        response = table.query(KeyConditionExpression='id = :id_smartgarden',
                               ExpressionAttributeValues={
                                   ':id_smartgarden': 'id_smartgarden'
                               },
                               ScanIndexForward=False,
                               Limit=1
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

        response = table.query(KeyConditionExpression='id = :id_smartgarden',
                               ExpressionAttributeValues={
                                   ':id_smartgarden': 'id_smartgarden'
                               },
                               ScanIndexForward=False,
                               Limit=20
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

        response = table.query(KeyConditionExpression='id = :id_smartgarden',
                               ExpressionAttributeValues={
                                   ':id_smartgarden': 'id_status'
                               },
                               ScanIndexForward=False,
                               Limit=1
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
